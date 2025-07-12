from pipeline.science.prompts.flashcards_prompts import FlashcardsPrompts

class Math_FlashcardsPrompts(FlashcardsPrompts):
    """
    Generates comprehensive, educational flashcard expansions for Mathematics with enhanced pedagogical focus.
    """
    _EXPANSION_TEMPLATE = (
        "For the course: {course_name}, provide an enhanced Example section for the keyword: {keyword}.\n"
        "{keyword}'s definition is: {definition}.\n\n"
        
        "Generate comprehensive mathematical examples based on the following guidelines:\n"
        "Max words for expansion: {expansion_length}\n\n"
        
        "1. **Mathematical Examples Section:**\n"
        "   - Provide exactly two distinct, real-world examples that demonstrate practical applications of {keyword}\n"
        "   - Label clearly as Example 1 and Example 2 for easy reference\n"
        "   - Use LaTeX syntax for all mathematical expressions:\n"
        "     * Inline formulas: $E = mc^2$\n"
        "     * Display formulas: $$\\frac{{a}}{{b}} = \\frac{{c}}{{d}}$$\n"
        "   - Include step-by-step breakdowns that show the mathematical reasoning process\n"
        "   - Use Markdown tables or diagrams when they enhance understanding\n"
        "   - Connect to real-world scenarios that students can relate to\n\n"
        
        "2. **Common Mistakes and Misconceptions Section:**\n"
        "   - Identify a typical error or misconception that students commonly make with {keyword}\n"
        "   - Explain why this mistake occurs (cognitive or conceptual reasons)\n"
        "   - Provide clear guidance on how to avoid or correct this mistake\n"
        "   - Include a brief example of the incorrect approach and the correct solution\n"
        "   - Use this as a learning opportunity to reinforce the correct understanding\n\n"
        
        "3. **Mathematical Content Requirements:**\n"
        "   - Use precise mathematical notation and terminology\n"
        "   - Define all variables and explain their meaning clearly\n"
        "   - Present mathematical reasoning in a clear, step-by-step manner\n"
        "   - Include verification methods to check if answers are reasonable\n"
        "   - Emphasize the mathematical thinking process, not just the answer\n\n"
        
        "4. **Formatting Requirements:**\n"
        "   - Use valid Markdown only (no code fences or '```markdown')\n"
        "   - Bold important mathematical terms and key concepts\n"
        "   - Use bullet points for step-by-step processes\n"
        "   - Include headers to organize different sections clearly\n"
        "   - Ensure professional mathematical presentation with clear, readable formatting\n\n"
        
        "Note: Focus on helping students develop both computational skills and conceptual understanding. The examples should be memorable, practical, and directly tied to the mathematical concept, while the common mistakes section should help prevent typical errors and build confidence in mathematical reasoning."
    )

    @staticmethod
    def flashcards_expansion_generation_prompt(course_name: str, chapter_name: str, keyword: str, definition: str, expansion_length: int) -> str:
        """
        Returns a comprehensive, educational flashcard expansion prompt specifically designed for Mathematics.
        
        This enhanced prompt focuses on:
        - Concrete mathematical examples with step-by-step reasoning
        - Common misconceptions and error prevention
        - Visual and interactive learning elements
        - Cross-concept connections and memory aids
        - Professional mathematical presentation standards
        """
        return Math_FlashcardsPrompts._EXPANSION_TEMPLATE.format(
            course_name=course_name,
            chapter_name=chapter_name,
            keyword=keyword,
            definition=definition,
            expansion_length=expansion_length,
        )