import os
from multiprocessing import Pool, freeze_support
from pipeline.dev_tasks import generate_flashcards

def gen_config():
    return {
        'llm_source': 'openai',
        # 'llm_source': 'anthropic',
        'temperature': 0,
        'creative_temperature': 0.5,
        'openai_key_dir': '.env',
        'anthropic_key_dir': '.env',
        'results_dir': 'pipeline/test_outputs/',
        'course_id_mapping_file': 'pipeline/test_outputs/course_id_mapping.json',
        'max_test_multiple_choice_questions_per_section': 1,
        'max_test_short_answer_questions_per_section': 1,
        'quiz_random_seed': 5,
        'regions': ['Example'],
        'flashcards_set_size': 30,
        'max_flashcards_size': 300,
        # 'quality_check_size': 30,
        'rich_content': False,
        'options_list': ['Mindmap', 'Table', 'Formula', 'Code'],
        'max_quiz_questions_per_section': 10,
        'definition_detail_level': 0,
        'expansion_detail_level': 0,
    }

# Parameter builders

def zero_shot_flashcards_para(course_description):
    para = {
        'zero_shot': True,
        'course_info': course_description,
        'keywords_per_chapter': 10,
    }
    para.update(gen_config())
    return para


def flashcards_para(main_filenames, supplementary_filenames=None):
    para = {
        'zero_shot': False,
        'book_dir': 'pipeline/test_inputs/',
        'main_filenames': main_filenames,
        'supplementary_filenames': supplementary_filenames,
        'chunk_size': 2000,
        'similarity_score_thresh': 0.8,
        'num_context_pages': 50,
        'keywords_per_page': 1.5,
        'page_set_size': 5,
        'overlapping': 0,
        'link_flashcards_size': 30,
    }
    para.update(gen_config())
    return para

# Worker function

def local_test(params):
    zero_shot, course_description, main_files, supplementary_files = params
    print(f"[PID {os.getpid()}] Starting generation for: {params!r}")
    try:
        if zero_shot:
            if course_description is None:
                raise ValueError('course_description cannot be None for zero-shot generation.')
            para = zero_shot_flashcards_para(course_description)
        else:
            if main_files is None:
                raise ValueError('main_filenames cannot be None for non-zero-shot generation.')
            para = flashcards_para(main_files, supplementary_files)
        generate_flashcards(para)
        print(f"[PID {os.getpid()}] Finished generation for: {params!r}")
    except Exception as e:
        print(f"[PID {os.getpid()}] Error for {params!r}: {e}")

# Main execution

if __name__ == '__main__':
    freeze_support()

    # Define test cases (uncomment or add as needed)
    test_cases = [
        # (True, 'level:"Beginner",subject:"",text:"I want to learn Calculus"', None, None),
    ]

       #  CS-specific test cases
    cs_test_cases = [
    # (True,  'level:"Intermediate",subject:"Computer Science",text:"I need help with Object‑Oriented Programming in Java"', None, None),
    # (True,  'level:"Advanced",subject:"Computer Science",text:"Explain the fundamentals of Machine Learning algorithms"', None, None),
    #(True,  'level:"Beginner",subject:"Computer Science",text:"How do relational databases work?"', None, None),
    #(True,  'level:"Intermediate",subject:"Computer Science",text:"Teach me about building RESTful APIs with Node.js"', None, None),
    # (True,  'level:"Advanced",subject:"Computer Science",text:"Dive into distributed systems design and CAP theorem"', None, None),
    # (True,  'level:"Beginner",subject:"Computer Science",text:"Introduction to HTML and CSS for web pages"', None, None),
    # (True,  'level:"Intermediate",subject:"Computer Science",text:"Understanding version control with Git and GitHub"', None, None),
    # (True,  'level:"Advanced",subject:"Computer Science",text:"Deep dive into neural network architectures and backpropagation"', None, None),
    # (True,  'level:"Intermediate",subject:"Computer Science",text:"Implementing data structures in C++: stacks, queues, and trees"', None, None),
    # (True,  'level:"Advanced",subject:"Computer Science",text:"Security best practices: encryption, hashing, and SSL/TLS protocols"', None, None),
    #(True,  'level:"Beginner",subject:"Computer Science",text:"Getting started with command-line interfaces and Bash"', None, None),
    #(True,  'level:"Intermediate",subject:"Computer Science",text:"Concurrency and parallelism in multithreaded applications"', None, None),
    #(True,  'level:"Advanced",subject:"Computer Science",text:"Design patterns in software engineering: Singleton, Observer, Factory"', None, None),
    #(True,  'level:"Intermediate",subject:"Computer Science",text:"Fundamentals of computer graphics and rendering pipelines"', None, None),
    #(True,  'level:"Advanced",subject:"Computer Science",text:"Quantum computing principles and qubit manipulation"', None, None),

    #(True, 'level:"Beginner",subject:"Computer Science",text:"Introduction to cloud computing and its applications"', None, None),
    #(True, 'level:"Intermediate",subject:"Computer Science",text:"Understanding DevOps practices and tools"', None, None),
    #(True, 'level:"Advanced",subject:"Computer Science",text:"Implementing continuous integration and deployment pipelines"', None, None),
    #(True, 'level:"Beginner",subject:"Computer Science",text:"Basics of software testing and quality assurance"', None, None),
    #(True, 'level:"Intermediate",subject:"Computer Science",text:"Exploring microservices architecture in software development"', None, None),
    #(True, 'level:"Advanced",subject:"Computer Science",text:"Designing scalable systems with load balancing and caching"', None, None),
    #(True, 'level:"Beginner",subject:"Computer Science",text:"Getting started with mobile app development"', None, None),
    #(True, 'level:"Intermediate",subject:"Computer Science",text:"Understanding containerization with Docker"', None, None),
    #(True, 'level:"Advanced",subject:"Computer Science",text:"Implementing machine learning models in production"', None, None),
    #(True, 'level:"Intermediate",subject:"Computer Science",text:"Exploring cybersecurity threats and mitigation strategies"', None, None),

#Old Prompts
    #(True, 'level:"Beginner",subject:"Computer Science",text:"Introduction to functional programming concepts"', None, None),
    #(True, 'level:"Intermediate",subject:"Computer Science",text:"Understanding recursion and its use cases"', None, None),
    #(True, 'level:"Advanced",subject:"Computer Science",text:"Implementing compiler front-ends and parsing techniques"', None, None),
    #(True, 'level:"Beginner",subject:"Computer Science",text:"Basics of encryption and public-key cryptography"', None, None),
    #(True, 'level:"Intermediate",subject:"Computer Science",text:"Developing single-page applications with React"', None, None),
    #(True, 'level:"Advanced",subject:"Computer Science",text:"Building fault-tolerant distributed systems"', None, None),

#Improved prompts
#(True, 'level:"Beginner",subject:"Computer Science",text:"Explain the core principles of functional programming (pure functions, immutability, higher-order functions) with a simple code example. Include a Python code snippet in a fenced code block demonstrating a pure function and immutability."', None, None)
#(True, 'level:"Intermediate",subject:"Computer Science",text:"Describe how recursion works and provide a real-world use case (e.g., tree traversal or factorial calculation). Compare its runtime complexity to an iterative solution, and include a code snippet showing both recursive and iterative versions in Python."', None, None)
#(True, 'level:"Advanced",subject:"Computer Science",text:"Detail the steps a compiler front-end takes to parse source code (lexical analysis, parsing, AST generation). Include an example grammar rule and a code snippet (in a language like Python or Java) that demonstrates how to generate and traverse a parse tree."', None, None)
#(True, 'level:"Beginner",subject:"Computer Science",text:"Outline the difference between symmetric and public-key encryption. Give an example of RSA key generation and encryption flow, and include a code snippet in Python showing how to generate keys and encrypt/decrypt a message."', None, None)
#(True, 'level:"Intermediate",subject:"Computer Science",text:"Explain how a React SPA renders components and handles state changes. Provide a short code snippet in JSX demonstrating a controlled form component with state management."', None, None)
#(True, 'level:"Advanced",subject:"Computer Science",text:"Discuss how fault tolerance is achieved in distributed systems (e.g., replication, consensus algorithms like Raft). Illustrate with a scenario of leader election and include a pseudo-code or code snippet in Go or Python showing the basic Raft election logic."', None, None)


#(True, 'level:"Intermediate",subject:"Computer Science",text:"Explain the concept of memoization, its benefits for recursive algorithms, and include a concise Python code example demonstrating caching."', None, None)
#(True, 'level:"Advanced",subject:"Computer Science",text:"Describe how Byzantine Fault Tolerance achieves consensus in distributed systems. Illustrate with a simplified message-flow diagram and outline its failure assumptions."', None, None)
#(True, 'level:"Beginner",subject:"Computer Science",text:"Outline the core principles of CSS Flexbox for responsive layouts. Provide a minimal HTML/CSS snippet that creates a centered navigation bar."', None, None)
#(True, 'level:"Intermediate",subject:"Computer Science",text:"Detail the steps of the TCP three-way handshake procedure, explain what happens when a handshake fails, and suggest recovery strategies."', None, None)

#(True, 'level:"Beginner",subject:"Computer Science",text:"Explain the HTTP request-response cycle and illustrate with a simple GET request example."', None, None)
#(True, 'level:"Intermediate",subject:"Computer Science",text:"Describe how indexing works in relational databases, compare B-tree vs. hash indexes, and discuss performance trade-offs."', None, None)
#(True, 'level:"Advanced",subject:"Computer Science",text:"Analyze the CAP theorem: explain Consistency, Availability, and Partition Tolerance with real-world distributed system examples."', None, None)
#(True, 'level:"Intermediate",subject:"Computer Science",text:"Explain event-driven architecture, demonstrate with a Node.js EventEmitter code snippet, and discuss scalability benefits."', None, None)
#(True, 'level:"Advanced",subject:"Computer Science",text:"Outline serverless computing architecture, describe cold start issues, and propose strategies to minimize latency."', None, None)

#(True, 'level:"Beginner",subject:"Computer Science",text:"Explain the concept of pointers in C, include pointer arithmetic, and provide a simple code example demonstrating pointer use."', None, None)
#(True, 'level:"Intermediate",subject:"Computer Science",text:"Describe the MapReduce programming model and illustrate with a word count example in pseudocode."', None, None)
#(True, 'level:"Advanced",subject:"Computer Science",text:"Detail the design and performance considerations of a lock-free concurrent queue data structure and compare it to a mutex-based implementation."', None, None)
#(True, 'level:"Intermediate",subject:"Computer Science",text:"Explain the role of middleware in distributed applications, provide an example architecture using message brokers like Kafka or RabbitMQ."', None, None)
#(True, 'level:"Advanced",subject:"Computer Science",text:"Analyze the security implications of SQL injection attacks and demonstrate how prepared statements prevent these vulnerabilities."', None, None)

#(True, 'level:"Beginner",subject:"Computer Science",text:"Explain how the quicksort algorithm works and include a Python code snippet implementing quicksort using recursion."', None, None)
#(True, 'level:"Intermediate",subject:"Computer Science",text:"Describe how to perform basic CRUD operations with a SQL database using Python\'s sqlite3 module, and include a code snippet showing creating a table, inserting, querying, updating, and deleting records."', None, None)
#(True, 'level:"Advanced",subject:"Computer Science",text:"Discuss thread synchronization challenges in multithreaded applications and include a Java code snippet demonstrating the use of synchronized blocks or locks to avoid race conditions."', None, None)
#(True, 'level:"Intermediate",subject:"Computer Science",text:"Explain JSON serialization and deserialization in Python, and include a code snippet showing how to convert a Python dictionary to a JSON string and back."', None, None)
#(True, 'level:"Advanced",subject:"Computer Science",text:"Detail how to perform web scraping with Python using BeautifulSoup, and include a code snippet that fetches a webpage, parses HTML elements, and extracts data."', None, None)

#(True, 'level:"Beginner",subject:"Computer Science",text:"Explain how a binary search tree works and include a Python code snippet for inserting a node."', None, None)
#(True, 'level:"Intermediate",subject:"Computer Science",text:"Describe how to implement a simple authentication system using JWTs in Node.js, and include a code snippet showing token generation and verification."', None, None)
#(True, 'level:"Advanced",subject:"Computer Science",text:"Discuss how to optimize database queries using indexing strategies, and include a SQL code snippet showing index creation and a performance comparison."', None, None)
#(True, 'level:"Intermediate",subject:"Computer Science",text:"Explain how event loop and callback mechanics work in JavaScript, and include a code snippet demonstrating asynchronous behavior with Promises."', None, None)
#(True, 'level:"Advanced",subject:"Computer Science",text:"Detail the steps to containerize a web application using Docker, and include a Dockerfile code snippet and explanation of each instruction."', None, None)
 
#(True, 'level:"Beginner",subject:"Computer Science",text:"Explain how a hash table works and include a Python code snippet demonstrating insert and lookup operations."', None, None)
#(True, 'level:"Intermediate",subject:"Computer Science",text:"Describe how to implement Dijkstra’s algorithm and include a Java code snippet showing the algorithm on a sample graph."', None, None)
#(True, 'level:"Advanced",subject:"Computer Science",text:"Detail the implementation of a basic neural network from scratch and include a Python code snippet for forward propagation and backpropagation."', None, None)
#(True, 'level:"Intermediate",subject:"Computer Science",text:"Explain how to set up a REST API using Flask in Python and include a code snippet for defining routes and handling JSON requests."', None, None)
#(True, 'level:"Advanced",subject:"Computer Science",text:"Discuss how to implement a blockchain data structure and include a JavaScript code snippet that demonstrates block creation and chain verification."', None, None)

#(True, 'level:"Intermediate",subject:"Computer Science",text:"Explain how to reverse a singly linked list in-place and include a Python code snippet demonstrating the algorithm."', None, None)
#(True, 'level:"Advanced",subject:"Computer Science",text:"Describe template metaprogramming in C++ and include a code snippet showing a compile-time factorial calculation using constexpr functions."', None, None)
#(True, 'level:"Intermediate",subject:"Computer Science",text:"Outline the OAuth2 authorization code flow in Node.js and include a JavaScript code snippet using Express and Passport.js to obtain and refresh access tokens."', None, None)
#(True, 'level:"Beginner",subject:"Computer Science",text:"Explain how CSS Grid works for layout design and include an HTML/CSS code snippet creating a responsive grid layout with named areas."', None, None)
#(True, 'level:"Advanced",subject:"Computer Science",text:"Detail how to deploy a containerized application to Kubernetes and include a YAML snippet defining a Deployment and Service with rolling update strategy."', None, None)

#(True, 'level:"Beginner",subject:"Computer Science",text:"Explain how breadth-first search (BFS) works on a graph and include a Python code snippet demonstrating BFS traversal."', None, None)
#(True, 'level:"Intermediate",subject:"Computer Science",text:"Describe how to write unit tests in Python using pytest and include a code snippet with test cases for a sample function."', None, None)
#(True, 'level:"Advanced",subject:"Computer Science",text:"Detail how to implement a simple custom memory allocator in C and include a code snippet showing malloc-like and free-like functions."', None, None)
#(True, 'level:"Intermediate",subject:"Computer Science",text:"Explain how async/await concurrency works in JavaScript and include a code snippet demonstrating fetching multiple APIs in parallel."', None, None)
#(True, 'level:"Advanced",subject:"Computer Science",text:"Outline how to build a WebSocket server in Node.js and include a code snippet that sets up a basic ws server and handles client messages."', None, None)



 ]

    all_cases = test_cases + cs_test_cases
    if not all_cases:
        print('No test cases defined! Populate test_cases or cs_test_cases and rerun.')
        exit(1)

    cpu_count = os.cpu_count() or 1
    print(f"Dispatching {len(all_cases)} jobs across {cpu_count} processes...")
    with Pool(processes=cpu_count) as pool:
        pool.map(local_test, all_cases)
    print('All flashcard generation jobs complete.')
