import re
import os
import json
import logging
import openai
from openai import RateLimitError

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain.output_parsers import OutputFixingParser

from pipeline.science.utils.cards import CardsUtil    # CardsUtil.combine_cards
from pipeline.science.utils.string import StringUtil    # StringUtil.ensure_utf8_encoding
from pipeline.science.meta_creater import Meta_Creater

from pipeline.science.prompts.zeroshot_flashcards_prompts import ZeroshotPrompts
# ZeroshotPrompts.topic_extraction_prompt
from pipeline.science.prompts.subjects_zeroshot_flashcards_prompts.STEM import STEM_ZeroshotPrompts
from pipeline.science.prompts.subjects_zeroshot_flashcards_prompts.social_sciences import SocialSciences_ZeroshotPrompts
from pipeline.science.prompts.subjects_zeroshot_flashcards_prompts.health_education import HealthEducation_ZeroshotPrompts
from pipeline.science.prompts.subjects_zeroshot_flashcards_prompts.business_economics import BusinessEconomics_ZeroshotPrompts
from pipeline.science.prompts.subjects_zeroshot_flashcards_prompts.humanities import Humanities_ZeroshotPrompts
from pipeline.science.prompts.subjects_zeroshot_flashcards_prompts.law import Law_ZeroshotPrompts
from pipeline.science.prompts.subjects_zeroshot_flashcards_prompts.CSDS import CSDS_ZeroshotPrompts
from pipeline.science.prompts.subjects_zeroshot_flashcards_prompts.Math import Math_ZeroshotPrompts
from pipeline.science.prompts.subjects_zeroshot_flashcards_prompts.language import Language_ZeroshotPrompts

logger = logging.getLogger("kzpipeline.science.zeroshot")

class Zeroshot_Flashcards(Meta_Creater):
    def __init__(self, para):
        super().__init__(para)
        logger.info("Initializing Zeroshot_Flashcards class.")
        self.max_flashcard_definition_words = int(para["definition_detail_level"] * 30 + 20)
        self.max_flashcard_expansion_words = int(para["expansion_detail_level"] * 100 + 100)
        self.keywords_per_chapter = para['keywords_per_chapter']
        self.flashcards_set_size = para["flashcards_set_size"]
        self.max_flashcards_size = para["max_flashcards_size"]
        self.flashcards_list = []
        self.prompt_class = self._determine_prompt_class()
        logger.info(f"Course ID hashed: {self.course_id}")
        logger.info(f"Creating directories: {self.flashcard_dir}, {self.quiz_dir}, {self.test_dir}, {self.course_meta_dir}")
        logger.info(f"Course meta directory: {self.course_meta_dir}")

    def _determine_prompt_class(self):
        """
        Determines the prompt class to use based on the subject.
        """
        subject = self.course_name_domain["subject"]
        logger.info("Extracting zero-shot topic.")
        if subject in ['Physics']:
            return STEM_ZeroshotPrompts()
        elif subject in ['Mathematics']:
            return Math_ZeroshotPrompts()
        elif subject in ['Literature', 'Philosophy', 'Art']:
            return Humanities_ZeroshotPrompts()
        elif subject in ['Economics', 'History', 'Geography', 'Political Science', 'Sociology']:
            return SocialSciences_ZeroshotPrompts()
        elif subject in ['Health', 'Physical Education']:
            return HealthEducation_ZeroshotPrompts()
        elif subject in ['Business', 'Finance', 'Accounting', 'Marketing']:
            return BusinessEconomics_ZeroshotPrompts()
        elif subject in ['Law']:
            return Law_ZeroshotPrompts()
        elif subject in ['Computer Science', 'Data Science']:
            return CSDS_ZeroshotPrompts()
        elif subject in ['Language']:
            return Language_ZeroshotPrompts()
        else:
            return ZeroshotPrompts()

    def create_chapters(self):
        """
        Function to create chapters for the given course.
        """
        llm = self.llm_advance
        # llm = self.llm_basic
        file_path = self.course_meta_dir +  "course_name_textbook_chapters.json"
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.course_name_textbook_chapters = json.load(file)
                # self.course_name_textbook_chapters = file.read()

        else:
            # Send the prompt to the API and get response
            parser = JsonOutputParser()
            error_parser = OutputFixingParser.from_llm(parser=parser, llm=self.llm_basic)
            prompt = self.prompt_class.chapters_generation_prompt()
            prompt = ChatPromptTemplate.from_template(prompt)
            chain = prompt | llm | error_parser
            response = chain.invoke({'extracted_course_name_domain': self.course_name_domain})
            self.course_name_textbook_chapters = StringUtil.ensure_utf8_encoding(response)
            file_path = self.course_meta_dir +  "course_name_textbook_chapters.json"
            # self.course_name_textbook_chapters["Course name"] = self.course_info
            self.course_name_textbook_chapters["Course name"] = self.course_name_domain["text"]
            with open(file_path, 'w') as file:
                json.dump(self.course_name_textbook_chapters, file, indent=2)

    def create_keywords(self):
        llm = self.llm_advance
        # llm = self.llm_basic
        self.create_chapters()

        if os.path.exists(self.flashcard_dir + "chapters_and_keywords.json"):
            with open(self.flashcard_dir + "chapters_and_keywords.json", 'r') as json_file:
                data_temp = json.load(json_file)
                self.chapters_list = data_temp["chapters_list"]
                self.keywords_list = data_temp["keywords_list"]
        else:
            with open(self.course_meta_dir + "course_name_textbook_chapters.json", 'r') as file:
                self.chapters_list = json.load(file)["Chapters"]
                self.raw_keywords_in_chapters = []
                self.raw_keywords_in_chapters = self.robust_generate_keywords(llm, self.course_name_domain, self.chapters_list, self.keywords_per_chapter)

                self.keywords_list = []

                parser = JsonOutputParser()
                error_parser = OutputFixingParser.from_llm(parser=parser, llm=self.llm_basic)
                prompt = self.prompt_class.keywords_cleaning_prompt()
                prompt = ChatPromptTemplate.from_template(prompt)
                try:
                    chain = prompt | llm | error_parser
                    response = chain.invoke({'chapters_list': self.chapters_list, 'raw_keywords_in_chapters': self.raw_keywords_in_chapters})
                    self.keywords_list = response["keywords"]
                except Exception as e:
                    logger.exception(f"Exception: {e}")
                    chain = prompt | self.llm_stable | error_parser
                    response = chain.invoke({'chapters_list': self.chapters_list, 'raw_keywords_in_chapters': self.raw_keywords_in_chapters})
                    self.keywords_list = response["keywords"]

                # logger.info("\nThe content in response chapter_list is: ", self.chapters_list)    #response["chapters_list"])
                # logger.info("\nThe content in response keywords_list is: ", self.keywords_list)   #response["keywords_list"])

                with open(self.course_meta_dir +  "raw_keywords_in_chapters.json", 'w') as file:
                    json.dump(self.raw_keywords_in_chapters, file, indent=2)
                with open(self.course_meta_dir +  "chapters_list.json", 'w') as file:
                    json.dump(self.chapters_list, file, indent=2)
                with open(self.course_meta_dir +  "keywords_list.json", 'w') as file:
                    json.dump(self.keywords_list, file, indent=2)

            # logger.info("\n\nself.chapters_list are:\n\n", self.chapters_list)
            # logger.info("\n\nself.keywords_list are:\n\n", self.keywords_list)

            data_temp = {
                "chapters_list": self.chapters_list,
                "keywords_list": self.keywords_list
            }
            data_temp = StringUtil.ensure_utf8_encoding(data_temp)

            # Save to JSON file
            with open(self.flashcard_dir + "chapters_and_keywords.json", 'w') as json_file:
                json.dump(data_temp, json_file, indent=4)
        return data_temp

    def create_flashcards(self, user_id="", course_id="", flashcards_write_cb=None, qform_expansion='explain_example'):
        llm = self.llm_basic
        max_flashcard_definition_words = self.max_flashcard_definition_words
        max_flashcard_expansion_words = self.max_flashcard_expansion_words
        full_flashcards_set = []

        if os.path.exists(self.flashcard_dir + "chapters_and_keywords.json"):
            with open(self.flashcard_dir + "chapters_and_keywords.json", 'r') as json_file:
                data_temp = json.load(json_file)
                self.chapters_list = data_temp["chapters_list"]
                self.keywords_list = data_temp["keywords_list"]
        else:
            self.create_keywords()

        for i in range(len(self.chapters_list)):
            if os.path.exists(self.flashcard_dir +  f'flashcards_set{i}.json'):
                with open(self.flashcard_dir + f'flashcards_set{i}.json', 'r') as file:
                    cards = json.load(file)
                    # flashcards_set_temp = json.load(file)
                    full_flashcards_set.append(cards)
            else:
                chapters_name_temp = self.chapters_list[i]
                keywords_list_temp = self.keywords_list[i]

                if os.path.exists(self.flashcard_dir + f'flashcards_set_def{i}.json'):
                    with open(self.flashcard_dir + f'flashcards_set_def{i}.json', 'r') as file:
                        cards_def = json.load(file)
                else:
                    # Generate definitions with one time prompt
                    cards_def = self.robust_generate_definitions(llm, keywords_list_temp, chapters_name_temp, self.course_name_textbook_chapters["Course name"], max_flashcard_definition_words)
                    cards_def = StringUtil.ensure_utf8_encoding(cards_def)

                if os.path.exists(self.flashcard_dir + f'flashcards_set_exp{i}.json'):
                    with open(self.flashcard_dir + f'flashcards_set_exp{i}.json', 'r') as file:
                        cards_exp = json.load(file)
                else:
                    try:
                        cards_exp = self.robust_generate_expansions(llm, keywords_list_temp, cards_def, chapters_name_temp, self.course_name_textbook_chapters["Course name"], max_flashcard_expansion_words, 3, regions = self.regions)
                        cards_exp = StringUtil.ensure_utf8_encoding(cards_exp)

                    except Exception as e:
                        logger.exception(f"Error generating expansions for chapter {chapters_name_temp}: {e}")
                        continue  # Skip this iteration and proceed with the next chapter

                if(self.rich_content == True):
                    # Generate rich content for the definitions
                    # llm = self.llm_advance
                    logger.info("Generating rich content...")
                    llm = self.llm_basic
                    rich_content = self.robust_generate_rich_content(llm, keywords_list_temp, cards_exp, chapters_name_temp, self.course_name_textbook_chapters["Course name"], options_list=self.options_list)
                    cards_exp = StringUtil.ensure_utf8_encoding(rich_content)

                cards = CardsUtil.combine_cards(cards_def, cards_exp)
                full_flashcards_set.append(cards)
                with open(self.flashcard_dir + f'flashcards_set_def{i}.json', 'w') as file:
                    json.dump(cards_def, file, indent=2)

                # # TEST
                # convert_json_to_html(self.course_name_domain, self.flashcard_dir + f'flashcards_set_def{i}.json', self.flashcard_dir + f'flashcards_set_def{i}.html')

                with open(self.flashcard_dir + f'flashcards_set_exp{i}.json', 'w') as file:
                    json.dump(cards_exp, file, indent=2)

                # # TEST
                # convert_json_to_html(self.course_name_domain, self.flashcard_dir + f'flashcards_set_exp{i}.json', self.flashcard_dir + f'flashcards_set_exp{i}.html')

                with open(self.flashcard_dir + f'flashcards_set{i}.json', 'w') as file:
                    json.dump(cards, file, indent=2)

            if(flashcards_write_cb is not None):
                flashcards_write_cb(user_id, course_id, i, cards, self.chapters_list)

        with open(self.flashcard_dir + f'full_flashcards_set.json', 'w') as file:
            json.dump(full_flashcards_set, file, indent=2)

        self.full_flashcards_set = full_flashcards_set
        return full_flashcards_set

    # Definition generation
    def generate_definitions(self, llm, keywords, chapter_name, course_name, definition_length):
        inputs = [{
                "course_name": course_name,
                "chapter_name": chapter_name,
                "keyword": keyword,
                "definition_length": definition_length
                } for keyword in keywords]
        parser = StrOutputParser()
        prompt = self.prompt_class.flashcards_definition_generation_prompt()
        prompt = ChatPromptTemplate.from_template(prompt)
        chain = prompt | llm | parser
        # (chain.abatch(inputs))
        # logger.info("Sending the request to the API..., for chapter_name: ", chapter_name)
        # results = await chain.abatch(inputs)
        results = chain.batch(inputs)
        # logger.info("Received the response from the API, for chapter_name: ", chapter_name)

        return dict(zip(keywords, results))

    # Definition generation with given number of attempts
    def robust_generate_definitions(self, llm, keywords, chapter_name, course_name, definition_length, max_attempts=3, if_parallel=True):
        attempt = 0
        # llm_sequence = [llm, self.llm_basic_backup_1, self.llm_basic_backup_2]
        llm_sequence = [llm]
        llm_index = 0

        while attempt < max_attempts:
            current_llm = llm_sequence[llm_index]
            try:
                if if_parallel:
                    return self.generate_definitions(current_llm, keywords, chapter_name, course_name, definition_length)
                else:
                    results = {}
                    for keyword in keywords:
                        result = self.generate_definitions(current_llm, [keyword], chapter_name, course_name, definition_length)
                        results.update(result)
                    return results
            except RateLimitError as e:
                logger.exception(f"RateLimitError encountered on attempt {attempt + 1} with model {current_llm}: {e}")
                if llm_index < len(llm_sequence) - 1:
                    llm_index += 1
                    logger.info(f"Switching to backup model: {llm_sequence[llm_index]}")
                else:
                    attempt += 1
                    if attempt == max_attempts:
                        logger.info(f"Failed to generate definitions after {max_attempts} attempts.")
                        raise Exception(f"Definitions generation failed after {max_attempts} attempts.")
            except Exception as e:
                logger.exception(f"Attempt {attempt + 1} failed for generating definitions: {e}")
                attempt += 1
                if attempt == max_attempts:
                    raise Exception(f"Definitions generation failed after {max_attempts} attempts.")

    # Expansion generation
    def generate_expansions(self, llm, keywords, defs, chapter_name, course_name, expansion_length, regions=["Example"]):
        def format_string(regions):
            markdown_content = "\n".join(
                [f'## {region}\n\nExample content for {region}.\n' for region in regions]
            )
            markdown_format_string = f"""
            {markdown_content}
            """
            return markdown_format_string

        def remove_first_sentence(text: str) -> str:
            """
            Removes the first line (up to and including the first newline character) ONLY IF
            it contains fewer than 5 words. If no newline is found and the entire text has
            fewer than 5 words, return an empty string; otherwise leave the text as is.
            """
            # Split into two parts at the first newline
            parts = text.split("\n", 1)
            
            # Check the word count of the first line
            first_line = parts[0].strip()
            word_count = len(first_line.split())
            
            # If the first line is shorter than 5 words, remove it
            if word_count < 5:
                # If there's a second part (i.e., a newline was found), return it
                if len(parts) > 1:
                    return parts[1].strip()
                else:
                    # No second part => just return an empty string
                    return ""
            else:
                # First line has 5 or more words => keep the entire text
                return text

        markdown_format_string = format_string(regions)

        inputs = [
            {
                "course_name": course_name,
                "chapter_name": chapter_name,
                "keyword": keyword,
                "definition": definition,
                "expansion_length": expansion_length,
                "markdown_format_string": markdown_format_string,
                "keyword_list": keywords
            }
            for keyword, definition in zip(keywords, defs)
        ]

        parser = StrOutputParser()
        error_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)

        prompt = self.prompt_class.flashcards_expansion_generation_prompt()
        system_prompt = self.prompt_class.system_prompt()
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", prompt),
            ]
        )
        chain = prompt | llm | error_parser

        # Generate expansions in batch
        results = chain.batch(inputs)

        # Remove the first sentence (up to first "\n") from each result
        cleaned_results = [remove_first_sentence(result) for result in results]

        return dict(zip(keywords, cleaned_results))

    # Expansion generation with given number of attempts
    def robust_generate_expansions(self, llm, keywords, defs, chapter_name, course_name, expansion_length, max_attempts=3, regions=["Example"], if_parallel=True):
        attempt = 0
        # llm_sequence = [llm, self.llm_basic_backup_1, self.llm_basic_backup_2]
        llm_sequence = [llm]
        llm_index = 0

        while attempt < max_attempts:
            current_llm = llm_sequence[llm_index]
            try:
                if if_parallel:
                    return self.generate_expansions(current_llm, keywords, defs, chapter_name, course_name, expansion_length, regions)
                else:
                    results = {}
                    for keyword in keywords:
                        result = self.generate_expansions(current_llm, [keyword], [defs[keyword]], chapter_name, course_name, expansion_length, regions)
                        results.update(result)
                    return results
            except RateLimitError as e:
                logger.exception(f"RateLimitError encountered on attempt {attempt + 1} with model {current_llm}: {e}")
                if llm_index < len(llm_sequence) - 1:
                    llm_index += 1
                    logger.info(f"Switching to backup model: {llm_sequence[llm_index]}")
                else:
                    attempt += 1
                    if attempt == max_attempts:
                        logger.info(f"Failed to generate expansions after {max_attempts} attempts.")
                        raise Exception(f"Expansions generation failed after {max_attempts} attempts.")
            except Exception as e:
                logger.exception(f"Attempt {attempt + 1} failed for generating expansions: {e}")
                attempt += 1
                if attempt == max_attempts:
                    raise Exception(f"Expansions generation failed after {max_attempts} attempts.")

    # Rich content options generation
    def generate_rich_content_options(self, llm, keywords, content_list, chapter_name, course_name, options_list = ["Mindmap", "Table", "Formula", "Code", "Image"]):
        """
        Generate rich content format options for the given keywords
        """
        options_map = self.prompt_class.rich_content_generation_prompts_map()
        inputs = [{
            "course_name": course_name,
            "chapter_name": chapter_name,
            "keyword": keyword,
            "content": content_list[keyword],
            "option": options_list,
        } for keyword in keywords]
        parser = StrOutputParser()
        error_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
        prompt = self.prompt_class.rich_content_generation_options_prompt()
        prompt = ChatPromptTemplate.from_template(prompt)
        chain = prompt | llm | error_parser
        # options = await chain.abatch(inputs)
        options = chain.batch(inputs)
        for i in range(len(options)):
            options[i] = re.sub(r'[^a-zA-Z0-9 ]', '', options[i])

        # logger.info("Options: ", options)

        formats = []
        for i in range(len(options)):
            if options[i] in options_list:
                formats.append(options_map[options[i]])
            else:
                formats.append("Sentence")
        
        # logger.info("Formats: ", formats)

        formats = dict(zip(keywords, formats))
        options = dict(zip(keywords, options))
        return formats, options

    # Rich content generation
    def generate_rich_content(self, llm, keywords, content_list, chapter_name, course_name, formats, options):
        """
        Generate rich content for the given keywords with the given format options
        """
        inputs = [{
            "course_name": course_name,
            "chapter_name": chapter_name,
            "keyword": keyword,
            "content": content_list[keyword],
            "format": formats[keyword],
            "option": options[keyword],
        } for keyword in keywords]
        parser = StrOutputParser()
        # parser = XMLOutputParser()
        error_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
        prompt = self.prompt_class.rich_content_generation_prompt()
        prompt = ChatPromptTemplate.from_template(prompt)
        chain = prompt | llm | error_parser
        # rich_contents = await chain.abatch(inputs)
        rich_contents = chain.batch(inputs)

        # final_roots = XmlUtil.nest_dict_to_xml(rich_contents)

        return dict(zip(keywords, rich_contents))

    # Rich content generation with given number of attempts
    def robust_generate_rich_content(self, llm, keywords, content_list, chapter_name, course_name, options_list=["Mindmap", "Table", "Formula", "Code", "Image"], max_attempts=3, if_parallel=True):
        attempt = 0
        # llm_sequence = [llm, self.llm_basic_backup_1, self.llm_basic_backup_2]
        llm_sequence = [llm]
        llm_index = 0

        while attempt < max_attempts:
            current_llm = llm_sequence[llm_index]
            try:
                if if_parallel:
                    formats, options = self.generate_rich_content_options(
                        current_llm, keywords, content_list, chapter_name, course_name, options_list=options_list
                    )
                    return self.generate_rich_content(
                        current_llm, keywords, content_list, chapter_name, course_name, formats, options
                    )
                else:
                    results = {}
                    for keyword in keywords:
                        formats, options = self.generate_rich_content_options(
                            current_llm, [keyword], content_list, chapter_name, course_name, options_list=options_list
                        )
                        result = self.generate_rich_content(
                            current_llm, [keyword], content_list, chapter_name, course_name, formats, options
                        )
                        results.update(result)
                    return results
            except RateLimitError as e:
                logger.exception(f"RateLimitError encountered on attempt {attempt + 1} with model {current_llm}: {e}")
                if llm_index < len(llm_sequence) - 1:
                    llm_index += 1
                    logger.info(f"Switching to backup model: {llm_sequence[llm_index]}")
                else:
                    attempt += 1
                    if attempt == max_attempts:
                        logger.info(f"Failed to generate rich content after {max_attempts} attempts.")
                        raise Exception(f"Rich content generation failed after {max_attempts} attempts.")
            except Exception as e:
                logger.exception(f"Attempt {attempt + 1} failed for generating rich content: {e}")
                attempt += 1
                if attempt == max_attempts:
                    logger.info(f"Failed to generate rich content after {max_attempts} attempts.")
                    raise Exception(f"Rich content generation failed after {max_attempts} attempts.")

    # keywords generation
    def generate_keywords(self, llm, course_name_domain, chapter_list, keywords_per_chapter):
        inputs = [{
                    "course_name_domain": course_name_domain,
                    "chapter_name": chapter,
                    "keywords_per_chapter": keywords_per_chapter,
                    "chapters_list": chapter_list
                } for chapter in chapter_list]
        parser = JsonOutputParser()
        error_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
        prompt = self.prompt_class.keywords_generation_prompt()
        prompt = ChatPromptTemplate.from_template(prompt)
        chain = prompt | llm | error_parser
        # (chain.abatch(inputs))
        # results = await chain.abatch(inputs)
        results = chain.batch(inputs)

        return dict(zip(chapter_list, results))

    # keywords generation with given number of attempts
    def robust_generate_keywords(self, llm, course_name_domain, chapter_list, keywords_per_chapter, max_attempts=3, if_parallel=True):
        attempt = 0
        # llm_sequence = [llm, self.llm_basic_backup_1, self.llm_basic_backup_2]
        llm_sequence = [llm]
        llm_index = 0

        while attempt < max_attempts:
            current_llm = llm_sequence[llm_index]
            try:
                if if_parallel:
                    return self.generate_keywords(current_llm, course_name_domain, chapter_list, keywords_per_chapter)
                else:
                    results = {}
                    for chapter in chapter_list:
                        result = self.generate_keywords(current_llm, course_name_domain, [chapter], keywords_per_chapter)
                        results.update(result)
                    return results
            except RateLimitError as e:
                logger.exception(f"RateLimitError encountered on attempt {attempt + 1} with model {current_llm}: {e}")
                if llm_index < len(llm_sequence) - 1:
                    llm_index += 1
                    logger.info(f"Switching to backup model: {llm_sequence[llm_index]}")
                else:
                    attempt += 1
                    if attempt == max_attempts:
                        logger.info(f"Failed to generate keywords after {max_attempts} attempts.")
                        raise Exception(f"Keywords generation failed after {max_attempts} attempts.")
            except Exception as e:
                logger.exception(f"Attempt {attempt + 1} failed for generating keywords: {e}")
                attempt += 1
                if attempt == max_attempts:
                    logger.info(f"Failed to generate keywords after {max_attempts} attempts.")
                    raise Exception(f"Keywords generation failed after {max_attempts} attempts.")

    def get_chapters_flashcards_list(self):
        return self.full_flashcards_set

    def get_all_flashcards_list(self):
        all_flashcards = {k: v for d in self.full_flashcards_set for k, v in d.items()}
        return all_flashcards

    def get_chapters_list(self):
        return self.chapters_list

    def get_hash_id(self):
        return self.course_id

    def get_course_name(self):
        if "Course name" in self.course_name_textbook_chapters:
            return self.course_name_textbook_chapters["Course name"]
        else:
            return ""
