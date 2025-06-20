from pipeline.science.prompts.flashcards_prompts import FlashcardsPrompts

class CSDS_FlashcardsPrompts(FlashcardsPrompts):
    """
    This class is used to generate prompts for the CS and DS domain
    •    Computer Science
    •    Data Science
    """
    PROMPTS = [
        (True, 'level:"Beginner",subject:"Computer Science",text:"Explain how breadth-first search (BFS) works on a graph and include a Python code snippet demonstrating BFS traversal."', None, None),
        (True, 'level:"Intermediate",subject:"Computer Science",text:"Describe how to write unit tests in Python using pytest and include a code snippet with test cases for a sample function."', None, None),
        (True, 'level:"Advanced",subject:"Computer Science",text:"Detail how to implement a simple custom memory allocator in C and include a code snippet showing malloc-like and free-like functions."', None, None),
        (True, 'level:"Intermediate",subject:"Computer Science",text:"Explain how async/await concurrency works in JavaScript and include a code snippet demonstrating fetching multiple APIs in parallel."', None, None),
        (True, 'level:"Advanced",subject:"Computer Science",text:"Outline how to build a WebSocket server in Node.js and include a code snippet that sets up a basic ws server and handles client messages."', None, None),
        (True, 'level:"Beginner",subject:"Computer Science",text:"Explain how to insert into a binary heap and include a Python code snippet demonstrating heap insertion using the heapq module."', None, None),
        (True, 'level:"Intermediate",subject:"Computer Science",text:"Describe the event sourcing pattern and include a JavaScript code snippet using Node.js to append and replay events from an event store."', None, None),
        (True, 'level:"Advanced",subject:"Computer Science",text:"Detail how Go channels enable concurrency and include a Go code snippet demonstrating communication between goroutines using channels."', None, None),
        (True, 'level:"Intermediate",subject:"Computer Science",text:"Explain how to build a simple GraphQL server in Node.js and include a code snippet defining a schema and resolver using graphql.js."', None, None),
        (True, 'level:"Advanced",subject:"Computer Science",text:"Outline how to implement async HTTP requests in Python with aiohttp and include a code snippet fetching multiple URLs concurrently."', None, None),
        (True, 'level:"Intermediate",subject:"Computer Science",text:"Explain the principles of dynamic programming and include a Python code snippet solving the Fibonacci sequence with memoization."', None, None),
        (True, 'level:"Advanced",subject:"Computer Science",text:"Describe how to implement OAuth2 token-based authentication in a Flask API and include a Python code snippet demonstrating token issuance and validation."', None, None),
        (True, 'level:"Beginner",subject:"Computer Science",text:"Outline the concept of finite state machines and include a JavaScript code snippet modeling a simple turnstile FSM."', None, None),
        (True, 'level:"Intermediate",subject:"Computer Science",text:"Explain how binary search operates on a sorted array and include a C code snippet demonstrating the iterative binary search function."', None, None),
        (True, 'level:"Advanced",subject:"Computer Science",text:"Detail how to create and apply decorators in Python and include a code snippet implementing a timing decorator to measure function execution time."', None, None),
        (True, 'level:"Intermediate",subject:"Computer Science",text:"Explain how to use regular expressions in Python and include a code snippet demonstrating pattern matching and data extraction."', None, None),
        (True, 'level:"Advanced",subject:"Computer Science",text:"Describe how to implement a basic garbage collector using the mark-and-sweep algorithm and include Python pseudocode that marks reachable objects and sweeps the rest."', None, None),
        (True, 'level:"Beginner",subject:"Computer Science",text:"Explain how to read from and write to files in Java and include a code snippet using FileReader and FileWriter."', None, None),
        (True, 'level:"Intermediate",subject:"Computer Science",text:"Outline how to implement a priority queue with a binary heap in JavaScript and include a code snippet showing insertion and removal operations."', None, None),
        (True, 'level:"Advanced",subject:"Computer Science",text:"Discuss how to profile a Python application’s performance and include a code snippet using the cProfile module to gather and display profiling results."', None, None),
    ]
