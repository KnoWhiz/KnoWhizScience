from pipeline.science.prompts.zeroshot_flashcards_prompts import ZeroshotPrompts

class CSDS_ZeroshotPrompts(ZeroshotPrompts):
    """
    This class generates zero-shot flashcard expansions for the CS & DS domains:
    • Computer Science
    • Data Science
    """

    # Precompiled prompt template for faster reuse
    _EXPANSION_TEMPLATE = (
        "For the course {course_name}, chapter {chapter_name}, keyword: **{keyword}** (definition: {definition}):\n"
        "\n"
        "**Example:**  \n"
        "Provide a concise real-world example that **does not** repeat the definition, and **must** include exactly one relevant code snippet inside a fenced Markdown block:\n"
        "\n"
        "```<language>\n"
        "# your code here\n"
        "```\n"
        "\n"
        "– If needed, use formulas wrapped in `$$ ... $$`.  \n"
        "– Keep the total length under {expansion_length} words.\n"
        "\n"
        "Respond in valid Markdown only."
    )

    @staticmethod
    def flashcards_expansion_generation_prompt(course_name: str, chapter_name: str, keyword: str, definition: str, expansion_length: int) -> str:
        """
        Returns a fully formatted flashcard expansion prompt, injecting parameters into the precompiled template.
        """
        # Directly format the precompiled string for minimal overhead
        return CSDS_ZeroshotPrompts._EXPANSION_TEMPLATE.format(
            course_name=course_name,
            chapter_name=chapter_name,
            keyword=keyword,
            definition=definition,
            expansion_length=expansion_length,
        )
