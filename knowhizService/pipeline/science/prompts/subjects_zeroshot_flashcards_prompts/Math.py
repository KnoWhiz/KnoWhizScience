from pipeline.science.prompts.zeroshot_flashcards_prompts import ZeroshotPrompts

class Math_ZeroshotPrompts(ZeroshotPrompts):
    """
    This class is used to generate prompts for the Mathamatics domain
    """
    @staticmethod
    # Step 5: Flashcards expansion generation
    def flashcards_expansion_generation_prompt():
        """
        Prompt for generating flashcards expansions for each keyword, requiring at least two different examples and a common mistake or misconception, with both summary and detailed formatting guidelines.
        """
        prompt = \
        """
        Complete the task step by step:
        For the course: {course_name}, chapter: {chapter_name}, provide an **Examples** section for the keyword: {keyword}.
        {keyword}'s definition is: {definition}.
        **Key requirements:**
        1. You are an expert in Mathematics.
        2. **Always include at least two different worked examples** relevant to {keyword}. Each example should be clearly labeled (e.g., Example 1, Example 2) and use LaTeX for all math notation:
           $$
           E = mc^2
           $$
        3. For each example, provide a step-by-step breakdown to enhance understanding.
        4. If helpful, include tables or diagrams using Markdown.
        5. **After the examples, add a section titled 'Common Mistake' or 'Misconception'** that describes a typical error or misunderstanding related to {keyword}, and how to avoid it.
        6. Do **not** include literal backticks around your final Markdown; just output ready-to-render Markdown.
        7. Max words for expansion: {expansion_length}
        8. Format the entire response as valid Markdown.
        ---
        **Formatting and Content Guidelines:**
        1. The section name is 'Example', which only includes a real world example to help memorize and understand the keyword in {course_name}.
        2. Please do not provide the definition of the keyword in the example.
        3. Within the example, provide a step-by-step breakdown only if it significantly enhances memorization and understanding of the concept.
        4. Within the example, if you need to display formulas, include them in LaTeX syntax formatted in markdown, as shown below:
            ----------------
            $$
            \\frac{{a}}{{b}} = \\frac{{c}}{{d}}
            $$
            ----------------
        5. Within the example, if you need to display tables, format them using markdown as follows:
            ----------------
            ## Table

            | Header 1   | Header 2   | Header 3   |
            |------------|------------|------------|
            | Row 1 Col 1| Row 1 Col 2| Row 1 Col 3|
            | Row 2 Col 1| Row 2 Col 2| Row 2 Col 3|
            | Row 3 Col 1| Row 3 Col 2| Row 3 Col 3|
            ----------------
        6. Do not include \"```markdown\" in the response. Final whole response must be in correct markdown format.
        7. Specify the text with intuitive markdown syntax like bold, italic, etc, bullet points, etc.
        8. For in-line formulas, use the syntax: $E = mc^2$. Remember must use double \"$\" for display formulas.
        """
        return prompt
    # def flashcards_expansion_generation_prompt():
    #     """
    #     Prompt for generating flashcards expansions for each keyword.
    #     """
    #     prompt = \
    #     """
    #     For the course: {course_name}, chapter: {chapter_name}, provide the expansions with a few pre-defined regions for the keyword: {keyword}.
    #     {keyword}'s definition is: {definition}.

    #     Organize the expansions in the style of a wiki page, and try to include more code snippets in Markdown syntax.
    #     The wiki page should focus more on practical and hands-on oriented content, do not talk about conceptional explanations.
    #     The wiki page should be at most {expansion_length} words long.
    #     For any computational related code, display it in descriptive pseudo-code instead, key point here is to show how the logic of the algorithm works.
    #     For algorithm snippets, must use triple backticks "```" for code blocks so we have structured display in markdown. 
    #     For each keywords' definition, aside from the definition, you must also concisely argue why this keyword is important, in correlation to the course name.
    #     """
    #     return prompt
