from pipeline.science.prompts.zeroshot_flashcards_prompts import ZeroshotPrompts

class STEM_ZeroshotPrompts(ZeroshotPrompts):
    """
    This class is used to generate prompts for the STEM domain
    •    Natural Sciences
        •    Biology
        •    Chemistry
        •    Physics
        •    Earth Science
        •    Environmental Science
        •    Astronomy
    •    Mathematics and Statistics
        •    Calculus
        •    Algebra
        •    Geometry
        •    Statistics
        •    Discrete Mathematics
        •    Differential Equations
    •    Engineering and Technology
        •    Mechanical Engineering
        •    Electrical Engineering
        •    Computer Science
        •    Civil Engineering
        •    Chemical Engineering
        •    Information Technology
    """
    
    @staticmethod
    # Step 5: Flashcards expansion generation
    def flashcards_expansion_generation_prompt():
        """
        Prompt for generating flashcards expansions for each keyword, specifically tailored for Physics domain within STEM.
        Requires at least two different examples and a common mistake or misconception, with both summary and detailed formatting guidelines.
        """
        prompt = \
        """
        Complete the task step by step:
        For the course: {course_name}, chapter: {chapter_name}, provide an **Examples** section for the keyword: {keyword}.
        {keyword}'s definition is: {definition}.
        **Key requirements:**
        1. You are an expert in Physics within the STEM domain.
        2. **Always include at least two different worked examples** relevant to {keyword}. Each example should be clearly labeled (e.g., Example 1, Example 2) and use LaTeX for all physics notation:
           $$
           F = ma
           $$
        3. For each example, provide a step-by-step breakdown to enhance understanding.
        4. If helpful, include tables, diagrams, or free-body diagrams using Markdown.
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
            \\vec{F} = -k\\vec{x}
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
        9. When applicable, include units and dimensional analysis in examples.
        10. For physics problems, always specify the coordinate system and reference frame when relevant.
        11. Focus on fundamental physics principles and their applications in real-world scenarios.
        12. Include vector notation and proper physics conventions when dealing with forces, velocities, and other vector quantities.
        """
        return prompt
