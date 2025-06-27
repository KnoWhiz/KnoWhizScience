from pipeline.science.prompts.zeroshot_flashcards_prompts import ZeroshotPrompts

class CSDS_ZeroshotPrompts(ZeroshotPrompts):
    """
    This class is used to generate prompts for the CS and DS domain
    •    Computer Science
    •    Data Science
    """
    @staticmethod
    def flashcards_expansion_generation_prompt():
        """
        Prompt for generating flashcards expansions for each keyword,
        always including one code snippet.
        """
        return """
For course {course_name}, chapter {chapter_name}, keyword **{keyword}** (definition: {definition}):

**Example:**  
Provide a concise real-world example that **does NOT** repeat the definition, and **always** include exactly one code snippet in a fenced Markdown block:

```<language>
# your code here

