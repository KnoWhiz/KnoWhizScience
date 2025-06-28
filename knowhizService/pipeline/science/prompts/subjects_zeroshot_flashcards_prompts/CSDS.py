from pipeline.science.prompts.zeroshot_flashcards_prompts import ZeroshotPrompts

class CSDS_ZeroshotPrompts(ZeroshotPrompts):
    """
    This class is used to generate prompts for the CS and DS domain:
    • Computer Science
    • Data Science
    """

    @staticmethod
    def flashcards_expansion_generation_prompt():
        """
        Prompt to generate flashcard expansions for each keyword,
        always including one code snippet.
        """
        return """
For the course {course_name}, chapter {chapter_name}, keyword: **{keyword}** (definition: {definition}):

**Example:**  
Provide a concise real-world example that **does not** repeat the definition, and **must** include exactly one relevant code snippet inside a fenced Markdown block:

```<language>
# your code here
```

– If needed, use formulas wrapped in `$$ ... $$`.  
– Keep the total length under {expansion_length} words.

Respond in valid Markdown only.
"""
