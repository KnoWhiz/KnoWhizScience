import os
import re
import json
import logging
import hashlib
import pandas as pd

from typing import Dict, List, Any, Optional
from langchain_community.document_loaders import PyMuPDFLoader, Docx2txtLoader
from langchain_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain.output_parsers import OutputFixingParser

from pipeline.science.api_handler import ApiHandler
from pipeline.science.prompt_handler import PromptHandler
from pipeline.science.anki_handler import AnkiLoader
from pipeline.science.links_handler import ExternalLinksHandler
from pipeline.science.prompts.flashcards_prompts import FlashcardsPrompts

logger = logging.getLogger("kzpipeline.science.doc_handler")

def split_filename(file_name_with_extension: str) -> str:
    """
    Splits the file name from its extension or returns 'link' if the input is a URL.

    Parameters:
    - file_name_with_extension (str): The full file name including its extension.

    Returns:
    - str: The extension of the file or 'link' if the input is a URL.

    Raises:
    - TypeError: If the input is not a string.
    - ValueError: If no extension is found in the file name and it's not a URL.
    """
    if not isinstance(file_name_with_extension, str):
        raise TypeError("Input must be a string.")

    # Regex to check if the string is a URL
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if re.match(url_pattern, file_name_with_extension):
        return "link"

    if '.' not in file_name_with_extension:
        raise ValueError("No extension found in the file name.")

    parts = file_name_with_extension.rsplit('.', 1)
    if not all(parts):
        raise ValueError("File name or extension is missing.")

    return parts[1]

def clean_string(url_string):
    """
    Use regular expression to replace sequences of non-letters with a single underscore
    # Example usage
    url_string = "https://example.com/path/to/page?query=123&other=abc"
    cleaned_string = clean_string(url_string)
    logger.info(cleaned_string)  # Output: "https_example_com_path_to_page_query_other_abc"
    """
    cleaned_string = re.sub(r'[^a-zA-Z]+', '_', url_string)
    return cleaned_string

class DocHandler:
    def __init__(self, para: Dict[str, Any]):
        """
        Initializes the document handler with configuration parameters.

        Parameters:
        - para (Dict[str, Any]): Configuration parameters including directories, filenames, and other settings.
        """
        self.book_dir = para['book_dir']
        self.main_filenames = self._ensure_list(para.get('main_filenames', []))

        self.chunk_size = int(para['chunk_size'])
        self.with_supplementary = para['supplementary_filenames'] is not None
        self.supplementary_filenames = self._ensure_list(para.get('supplementary_filenames', []))
        self.nMain = len(self.main_filenames)
        self.nSupp = len(self.supplementary_filenames)
        self.results_dir = para['results_dir']
        self.course_id_mapping_file = para['course_id_mapping_file']
        # Extract the directory path from the full file path
        dir_path = os.path.dirname(para['course_id_mapping_file'])
        logger.info(dir_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if not os.path.exists(self.course_id_mapping_file):
            with open(self.course_id_mapping_file, 'w') as f:
                json.dump({}, f, indent=2)
        self.api = ApiHandler(para)
        self.prompt = PromptHandler(self.api)
        self._init_file_handling()

    def _ensure_list(self, input_val: Any) -> List[str]:
        """Ensures the provided input is a list of strings."""
        if isinstance(input_val, list):
            return input_val
        if isinstance(input_val, str) and input_val:
            return [input_val]
        return []

    def _init_file_handling(self):
        """Sets up file handling operations."""
        self._extract_file_types()
        self._retrieve_file_dirs()

        self._loader_map()
        self._load_files()
        if not self._check_documents_quality(self.main_docs + self.supp_docs):
            logger.info("Quality check failed. Stopping the application.")
            raise Exception("Quality check failed")
        else:
            logger.info("Quality check passed.")
        self._create_course_output_dirs()
        self.main_docs_pages = self._get_page_numbers(self.main_docs)
        self.supp_docs_pages = self._get_page_numbers(self.supp_docs)
        self.indx_page_docs = self.locate_and_save_index_pages(self.main_docs, self.main_filenames, self.main_file_types+self.supplementary_file_types)
        self.cont_page_docs = self.locate_and_save_contents_pages(self.main_docs, self.main_filenames)
        self.main_embedding = self.create_and_store_embeddings(self.main_docs, self.main_filenames)
        self.supp_embedding = self.create_and_store_embeddings(self.supp_docs, self.supplementary_filenames)
        if(self.main_file_types[0] != 'apkg'):
            self.infer_course_name_domain(self.main_docs[0], 'basic')
        else:
            self.course_name_domain = {
                "context": "None",
                "level": "None",
                "subject": "Anki",
                "course_name_domain": "Anki"
                }

    def _retrieve_file_dirs(self):
        """
        Populates `main_file_dirs` and `supplementary_file_dirs` lists with the full paths
        for main and supplementary files, respectively.
        """
        # self.main_file_dirs = [os.path.join(self.book_dir, file) for file in self.main_filenames]
        # self.supplementary_file_dirs = [os.path.join(self.book_dir, file) for file in self.supplementary_filenames]
        self.main_file_dirs = [
            file if file_type == 'link' else os.path.join(self.book_dir, file)
            for file, file_type in zip(self.main_filenames, self.main_file_types)
        ]
        self.supplementary_file_dirs = [
            file if file_type == 'link' else os.path.join(self.book_dir, file)
            for file, file_type in zip(self.supplementary_filenames, self.supplementary_file_types)
        ]
        # logger.info(f"main_file_dirs: {self.main_file_dirs}")
        # logger.info(f"supplementary_file_dirs: {self.supplementary_file_dirs}")

    def _extract_file_types(self):
        """
        Populates `main_file_types` and `supplementary_file_types` with the file types (extensions)
        of main and supplementary files, respectively. This method relies on the `split_filename`
        function to extract the file type from each filename.
        """
        self.main_file_types = [split_filename(file) for file in self.main_filenames]
        self.supplementary_file_types = [split_filename(file) for file in self.supplementary_filenames]
        # logger.info(f"main_file_types: {self.main_file_types}")
        # logger.info(f"supplementary_file_types: {self.supplementary_file_types}")

    def _loader_map(self, pdf_loader=PyMuPDFLoader, docx_loader=Docx2txtLoader, apkg_loader=AnkiLoader, link_loader=ExternalLinksHandler):
        """Initializes the mapping of file types to their respective loaders."""
        self.loader_map = {
            'pdf': pdf_loader,
            'docx': docx_loader,
            'apkg': apkg_loader,
            'link': link_loader
        }

    def _load_files(self):
        """
        Loads documents for both main and supplementary files using the specified loaders.
        This method assumes that `_retrieve_file_dirs` and `_extract_file_types` have already
        been called to prepare the file paths and types.
        """
        self.main_docs = self._load_file_group(self.main_file_dirs, self.main_file_types)
        self.supp_docs = self._load_file_group(self.supplementary_file_dirs, self.supplementary_file_types)

        # logger.info(f"main_docs: {self.main_docs}")
        # logger.info(f"supp_docs: {self.supp_docs}")

    def _load_file_group(self, file_paths: List[str], file_types: List[str]) -> List[Optional[Any]]:
        """
        Loads a group of files specified by their paths and types.

        Parameters:
        - file_paths (List[str]): The full paths to the files to be loaded.
        - file_types (List[str]): The types of the files to be loaded, corresponding by index to `file_paths`.

        Returns:
        - List[Optional[Any]]: A list of loaded documents or None for each file that failed to load.
        """
        docs = []

        for path, type_ in zip(file_paths, file_types):
            try:
                if type_ in self.loader_map:
                    loader_class = self.loader_map[type_]
                    doc = loader_class(path).load()
                    # logger.info(f"Loaded document: ", doc)
                    docs.append(doc)
                else:
                    logger.info(f"Unsupported document type: {type_} for file {path}")
                    docs.append(None)
            except Exception as e:
                logger.exception(f"Failed to load document {path} of type {type_}: {e}")
                docs.append(None)

        # logger.info(f"Loaded documents: {docs}")
        return docs

    def _percent_blank(self, doc: Any, type = None) -> float:
        """
        Calculates the percentage of blank pages in a document.

        Parameters:
        - doc (Any): The document to analyze.

        Returns:
        - float: The percentage of blank pages within the document.
        """
        # Skip quality check if the file is an Anki flashcard deck. We should only accept Anki flashcard decks as main files (not mixed).
        if(type == 'apkg' or type == 'link'):
            return 0.0

        if not doc or not hasattr(doc, "__iter__") or not len(doc):
            return 0.0

        blank_count = sum(1 for page in doc if not getattr(page, "page_content", "").strip())
        total_pages = len(doc)
        return (blank_count / total_pages) * 100.0 if total_pages else 0.0

    def _check_documents_quality(self, documents: List[Any], blank_perc: int = 15) -> bool:
        """
        Iterates over a list of documents to check if each meets the specified quality criteria 
        based on the percentage of blank pages, logging outcomes and determining if the batch 
        passes quality checks.

        Parameters:
        - documents (List[Any]): The documents to check.
        - blank_perc (int): The threshold percentage of blank pages allowed.

        Returns:
        - bool: True if all documents pass the quality check, False otherwise.
        """
        failed_checks = []
        errors = []

        for i, doc in enumerate(documents):
            try:
                percent_blank = self._percent_blank(doc, type=self.main_file_types[i] if i < self.nMain else self.supplementary_file_types[i-self.nMain])
                logger.info(f"Document {i} has {percent_blank}% blank pages.")
                if percent_blank > blank_perc:
                    logger.info(f"Document {i} exceeds the allowed {blank_perc}% of blank pages with {percent_blank}% blank.")
                    failed_checks.append(i)
            except Exception as e:
                logger.exception(f"Error during quality check for document {i}: {e}")
                errors.append(i)

        if errors:
            logger.info(f"Errors occurred in {len(errors)} document quality checks.")
            return False
        if failed_checks:
            logger.info(f"{len(failed_checks)} documents failed the quality check.")
            return False

        logger.info("All documents passed the quality check without errors.")
        return True

    def _hash_document_id(self):
        """
        Generates a unique SHA-224 hash based on the content of documents within the handler.
        This method combines the text content of all main and supplementary documents,
        computes a SHA-224 hash, and checks against existing course IDs to avoid duplicates.
        If the generated ID is new, it is saved along with the filenames of the documents.

        Returns:
            bool: True if the generated course ID already exists, False otherwise.
        """
        # Initialize a SHA-224 hashlib object
        sha224_hash = hashlib.sha224()
        # Combine and hash the content of all documents
        for doc in self.main_docs:
            sha224_hash.update('main'.encode("utf-8"))
            for page_text in doc:
                try:
                    sha224_hash.update(page_text.page_content.encode("utf-8"))
                except AttributeError:
                    sha224_hash.update(str(page_text).encode("utf-8"))

        for doc in self.supp_docs:
            # logger.info(f"self.supp_docs: {self.supp_docs}")
            sha224_hash.update('supp'.encode("utf-8"))
            if(doc != None):
                for page_text in doc:
                    try:
                        sha224_hash.update(page_text.page_content.encode("utf-8"))
                    except AttributeError:
                        sha224_hash.update(str(page_text).encode("utf-8"))
        # Compute the final hash value
        self.course_id = sha224_hash.hexdigest()
        # Load existing course IDs to check for duplicates
        with open(self.course_id_mapping_file, 'r') as file:
            self.existing_ids = json.load(file)
        # Check if the generated course ID already exists
        if self.course_id in self.existing_ids:
            return True
        # Save the new course ID with associated filenames if it's new
        self.existing_ids[self.course_id] = self.main_filenames + self.supplementary_filenames
        with open(self.course_id_mapping_file, "w") as outfile:
            json.dump(self.existing_ids, outfile, indent=2)
        return False

    def _create_course_output_dirs(self):
        """
        Creates directory structures for storing course outputs.

        Based on the generated course ID, this method constructs directories for
        flashcards, quiz, test, course metadata, and book embeddings. If the course ID is new,
        the directories are created under the specified results directory.
        """
        # Check if course ID exists and create directories if it doesn't
        self.course_id_exist = self._hash_document_id()
        # Define directory paths for different course outputs
        self.test_dir = os.path.join(self.results_dir, "test", self.course_id)
        self.quiz_dir = os.path.join(self.results_dir, "quiz", self.course_id)
        self.flashcard_dir = os.path.join(self.results_dir, "flashcards", self.course_id)
        self.course_meta_dir = os.path.join(self.results_dir, "course_meta", self.course_id)
        self.book_embedding_dir = os.path.join(self.results_dir, "book_embedding", self.course_id)
        if not self.course_id_exist:
            os.makedirs(self.test_dir, exist_ok=True)
            os.makedirs(self.quiz_dir, exist_ok=True)
            os.makedirs(self.flashcard_dir, exist_ok=True)
            os.makedirs(self.course_meta_dir, exist_ok=True)
            os.makedirs(self.book_embedding_dir, exist_ok=True)

    def _get_page_numbers(self, documents):
        """
        Calculate and return the number of pages for each document in a list.

        This method assumes each document's length represents its number of pages.

        Parameters:
        - documents (list): A list of documents, where each document is assumed to be
        a collection or sequence type with a length that indicates its page count.

        Returns:
        - list: A list of integers representing the page count for each document.
        """
        page_counts = [len(doc) for doc in documents]
        return page_counts

    def locate_and_save_index_pages(self, documents, doc_names, doc_types=None):
        """
        self.indx_page_docs = self.locate_and_save_index_pages(self.main_docs, self.main_filenames)

        Identifies pages within the last 30 pages of documents that contain the word 'index',
        excluding pages with specific phrases. This method focuses on locating index sections
        typically found at the end of books. The identified index pages are then saved to CSV files,
        named based on the document names, ensuring easy tracking and retrieval.

        Args:
            documents (list): A list of document page objects, where each object has a 'page_content' attribute.
            doc_names (list): A list of document names, each used to generate a CSV file name.

        Returns:
            list: A list of pandas DataFrames, each representing the index page information for a document.
        """
        dfs = []  # List to store DataFrames for each document

        for document, doc_name, doc_type in zip(documents, doc_names, doc_types):
            index_pages = {}
            excluded_phrases = ["author index", "symbol index", "index to appendix"]

            # Identify potential index pages
            for i, page in enumerate(document):
                # logger.info("\nIdentify potential index pages...")
                content_lower = page.page_content.lower()
                if "index" in content_lower[:50] and not any(phrase in content_lower for phrase in excluded_phrases):
                    index_pages[i] = page

            if not index_pages:
                df = self._write_index_info_to_csv([], [], doc_name)
                dfs.append(df)
                continue

            # Determine if the identified pages are within the last 30 pages
            book_total_pages = len(document)
            index_page_nums = [page_num for page_num in index_pages if page_num >= book_total_pages - 30]

            if not index_page_nums:
                df = self._write_index_info_to_csv([], [], doc_name)
                dfs.append(df)
                continue

            # Retrieve the pages from the minimum index page number to the end of the document
            min_index_page_num = min(index_page_nums)
            final_index_pages = {page_num: document[page_num] for page_num in range(min_index_page_num, book_total_pages)}
            df = self._write_index_info_to_csv(list(final_index_pages.keys()), list(final_index_pages.values()), doc_name)
            dfs.append(df)
            logger.info(f"Processed index pages for {doc_name}.")

        # logger.info(f"dfs: {dfs}")
        return dfs

    def _write_index_info_to_csv(self, page_nums, page_docs, doc_name):
        """
        Creates or overwrites a CSV file with the provided index page information, named according
        to the document name. This file documents the page numbers and content of index pages identified
        in a document.

        Args:
            page_nums (list): The numbers of the pages identified as part of the index.
            page_docs (list): The content of the pages identified as part of the index.
            doc_name (str): The name of the document, which is used to name the CSV file.

        Returns:
            pandas.DataFrame: A DataFrame of the data written to the CSV, facilitating further analysis
                            or processing within the program.
        """
        doc_name = clean_string(doc_name)

        if not page_nums:  # If there are no pages, write 'no index' to the file
            df = pd.DataFrame({'index_pages': [None], 'index_docs': [None]})
        else:
            df = pd.DataFrame({'index_pages': page_nums, 'index_docs': [str(doc) for doc in page_docs]})
        try:
            df.to_csv(f"{self.course_meta_dir}/{doc_name}_index_docs.csv", index=False)
        except Exception as e:
            logger.exception(f"Error writing index info to CSV: {e}")

        logger.info("\nFinished writing index info to CSV.")
        return df

    def locate_and_save_contents_pages(self, documents, doc_names):
        """
        Identifies pages within the first 50 pages of documents that contain the word 'contents',
        excluding pages with specific phrases. This method focuses on locating contents sections
        typically found at the end of books. The identified contents pages are then saved to CSV files,
        named based on the document names, ensuring easy tracking and retrieval.

        Args:
            documents (list): A list of document page objects, where each object has a 'page_content' attribute.
            doc_names (list): A list of document names, each used to generate a CSV file name.

        Returns:
            list: A list of pandas DataFrames, each representing the contents page information for a document.
        """
        dfs = []  # List to store DataFrames for each document

        for document, doc_name in zip(documents, doc_names):
            contents_pages = {}
            excluded_phrases = []

            # Identify potential contents pages
            for i, page in enumerate(document):
                # logger.info("\nIdentify potential contents pages...")
                content_lower = page.page_content.lower()
                if "contents" in content_lower[:50] and not any(phrase in content_lower for phrase in excluded_phrases):
                    contents_pages[i] = page

            if not contents_pages:
                df = self._write_contents_info_to_csv([], [], doc_name)
                dfs.append(df)
                continue

            # Determine if the identified pages are within the first 50 pages
            book_total_pages = len(document)
            contents_page_nums = [page_num for page_num in contents_pages if page_num <= 50]

            if not contents_page_nums:
                df = self._write_contents_info_to_csv([], [], doc_name)
                dfs.append(df)
                continue

            # Retrieve the pages from 0 to the last contents page number
            min_contents_page_num = max(contents_page_nums)
            final_contents_pages = {page_num: document[page_num] for page_num in range(0, min_contents_page_num)}
            df = self._write_contents_info_to_csv(list(final_contents_pages.keys()), list(final_contents_pages.values()), doc_name)
            dfs.append(df)
            logger.info(f"Processed contents pages for {doc_name}.")
        return dfs

    def _write_contents_info_to_csv(self, page_nums, page_docs, doc_name):
        """
        Creates or overwrites a CSV file with the provided contents page information, named according
        to the document name. This file documents the page numbers and content of contents pages identified
        in a document.

        Args:
            page_nums (list): The numbers of the pages identified as part of the contents.
            page_docs (list): The content of the pages identified as part of the contents.
            doc_name (str): The name of the document, which is used to name the CSV file.

        Returns:
            pandas.DataFrame: A DataFrame of the data written to the CSV, facilitating further analysis
                            or processing within the program.
        """
        doc_name = clean_string(doc_name)

        if not page_nums:
            df = pd.DataFrame({'contents_pages': [None], 'contents_docs': [None]})
        else:
            df = pd.DataFrame({'contents_pages': page_nums, 'contents_docs': [str(doc) for doc in page_docs]})
        try:
            df.to_csv(f"{self.course_meta_dir}/{doc_name}_contents_docs.csv", index=False)
        except Exception as e:
            logger.exception(f"Error writing contents info to CSV: {e}")
        return df

    def _split_doc_into_chunks(self, document):
        """
        Splits a book into chunks of specified size with no overlap.

        Args:
            document (str): The text of the document to be split.

        Returns:
            list: A list of text chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=0)
        chunks = text_splitter.split_documents(document)
        logger.info(f'Now you have {len(chunks)} chunks from the document.')
        return chunks

    def create_and_store_embeddings(self, documents, filenames):
        """
        Creates and stores embeddings for each provided document if they do not already exist.
        Checks for existing embeddings to avoid redundant computations.

        Args:
            documents (list): List of document texts to process.
            filenames (list): Corresponding list of filenames used for storing the embeddings.
        """
        embedding_list = []
        for document, document_name, types in zip(documents, filenames, self.main_file_types):
            embedding_file_path = os.path.join(self.book_embedding_dir, clean_string(document_name) + ".faiss")
            if os.path.exists(embedding_file_path):
                # Load the existing FAISS index
                print(f"Loading existing embedding for {document_name}.")
                logger.info(f"Loading existing embedding for {document_name}.")
                # db = FAISS.load_local(embedding_file_path, AzureOpenAIEmbeddings())
                embeddings = AzureOpenAIEmbeddings(deployment="text-embedding-3-large",
                                                model="text-embedding-3-large",
                                                azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
                                                openai_api_type="azure",
                                                chunk_size=1)
                db = FAISS.load_local(embedding_file_path, embeddings, allow_dangerous_deserialization=True)
                embedding_list.append(db)

            elif(types != 'apkg'):
                print(f"Creating new embedding for {document_name}.")
                logger.info(f"Creating new embedding for {document_name}.")
                # embeddings = AzureOpenAIEmbeddings()
                embeddings = AzureOpenAIEmbeddings(deployment="text-embedding-3-large",
                                                model="text-embedding-3-large",
                                                azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
                                                openai_api_type="azure",
                                                chunk_size=1)
                
                chunks = self._split_doc_into_chunks(document)
                db = FAISS.from_documents(chunks, embeddings)
                db.save_local(embedding_file_path)
                embedding_list.append(db)
            logger.info(f"Embedding file for {document_name} is ready for use.")

        return embedding_list

    def infer_course_name_domain(self, doc, model_version, pages=20):
        """
        Infers the course name and its domain from the document's content, utilizing a language model for inference.

        Parameters:
        - doc: The document from which to infer the course name and domain.
        - pages (int): The number of pages to consider from the beginning of the document for inference.

        Returns:
        - str: The inferred course name and domain.
        """
        course_meta_file_path = os.path.join(self.course_meta_dir, "course_name_domain.json")

        if (self.main_file_types[0] != 'apkg' and self.main_file_types[0] != 'link'):
            # chunk = self.prompt.split_prompt(str(doc[:pages]), model_version, return_first_chunk_only=True)[0]
            text_content = ''.join([page.page_content for page in doc[:pages]])
            custom_token_limit = int(self.api.models[model_version]['context_window']/1.2)
            chunk = self.prompt.split_prompt(text_content, model_version, custom_token_limit=custom_token_limit, return_first_chunk_only=True)[0]
            self.textbook_content_pages = chunk
            # print("The chunk is: ", chunk)
            # self.textbook_content_pages = self.cont_page_docs[0]['contents_docs']
        elif (self.main_file_types[0] == "link"):
            chunk = str([page.page_content for page in doc])
            self.textbook_content_pages = chunk
        elif (self.main_file_types[0] == 'apkg'):
            chunk = str([page.anki_content["Question"] for page in doc])
            self.textbook_content_pages = chunk
        # Check if the course meta file exists and read from it if it does
        if os.path.exists(course_meta_file_path):
            with open(course_meta_file_path, 'r') as file:
                self.course_name_domain = json.load(file)
                return
        #infer course name
        llm = self.api.models[model_version]['instance']
        parser1 = JsonOutputParser()
        error_parser = OutputFixingParser.from_llm(parser=parser1, llm=llm)
        prompt1 = ChatPromptTemplate.from_template(
            """
            Based on texts in the beginning of a course document ```{doc}```, please answer the following question:
            If "Context" is a restrictive description of the course, and "subject" is the general topic of the course,
            and "text" is the detailed description about the document that this user wants to learn.
            Please answer: what is the learning topic of this course should be, by combining "context", "subject", and "text".
            For example, The output can be like this:
            ```
            {{
            "context": "Bayesian"
            "level": "Beginner"
            "subject": "Computer Science"
            "text": "Bayesian machine learning techniques"
            "title": "Bayesian Machine Learning"
            }}
            ```
            The response should be formated as json:
            ```json
            {{
            "context": <what is the context of this course>,
            "level": <what is the difficulty level of this course, like beginner level, medium level, or advanced level etc.>,
            "subject": <what is the subject of this course, options include {subject_options}>,
            "course_name_domain": <what is the detailed full description for the topic of this course (will be auto generated if not provided)>
            "title": <what is the title of this course, will be auto generated if not provided>
            }}
            ```
            """
        )
        # chain 1: input= doc and output= course_name
        chain1 = prompt1 | llm | parser1
        try:
            response = chain1.invoke({'doc': chunk, 'subject_options': FlashcardsPrompts.subject_options()})
            # logger.info(f"doc: {chunk}")
        except Exception as e:
            logger.exception(f"exception: {e}")
            summary = self.prompt.summarize_prompt(chunk, 'basic', custom_token_limit=int(self.api.models[model_version]['context_window']/1.2))
            response = chain1.invoke({'doc': summary, 'subject_options': FlashcardsPrompts.subject_options()})

        self.course_name_domain = response
        with open(course_meta_file_path, 'w') as file:
            json.dump(self.course_name_domain, file, indent=2)
        return self.course_name_domain
