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
        always including at least one code snippet.
        """
        return """
        Complete the task step by step:

        For the course: {course_name}, chapter: {chapter_name}, provide an Example section for the keyword: {keyword}.
        {keyword}'s definition is: {definition}.

        **Key requirements:**
        1. You are an expert in Computer Science & Data Science.
        2. **Always include at least one code snippet** relevant to {keyword}, formatted in Markdown fenced code blocks:
           ```<language>
           // your code here
           ```
        3. The section name must be **Example** and should **not** repeat the definition.
        4. Use step‑by‑step explanations only when they clearly improve understanding.
        5. If you show formulas, wrap them in LaTeX double‑dollar syntax:
           $$
           E = mc^2
           $$
        6. If you include tables, use Markdown tables as follows:
           | A | B | C |
           |--|--|--|
           |…|…|…|
        7. Do **not** include literal backticks around your final Markdown; just output ready‑to‑render Markdown.

        Max words for expansion: {expansion_length}

        Format the entire response as valid Markdown.
        """

