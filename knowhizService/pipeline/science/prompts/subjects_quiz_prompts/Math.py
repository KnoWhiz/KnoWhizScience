from pipeline.science.prompts.quiz_prompts import QuizPrompts

class Math_QuizPrompts(QuizPrompts):
    """
    Generates advanced, integrated mathematics quiz prompts that require students to synthesize multiple mathematical concepts for deeper understanding.
    """

    _DEFINITION_TEMPLATE = (
        """
        You are a university-level mathematics instructor creating a **definition-based multiple-choice question** that requires integrating at least two different mathematical topics.

        Given the course: {course_name}, chapter: {chapter_name}, and concept: {keyword}, generate one question that tests the student's understanding of the **term’s definition** in a context that combines it with another relevant mathematical concept.

        Guidelines:
        - The question must require the student to use knowledge from at least two different mathematical areas (e.g., algebra and geometry, calculus and statistics).
        - Provide a real-world or cross-topic scenario where these concepts interact.
        - Emphasize mathematical reasoning and conceptual depth, not just recall.
        - Use clear mathematical notation (LaTeX inline: $...$) where appropriate.
        - Avoid trick questions; focus on clarity and depth.
        - Provide exactly **1 correct answer** and **3 plausible distractors** based on common student confusion.
        - Include a brief explanation for why the correct answer is right and the others are not.

        Example output structure:
        {{
          "question": "...",
          "choices": {{
            "A": "...",
            "B": "...",
            "C": "...",
            "D": "..."
          }},
          "correct_answer": "B",
          "explanation": "..."
        }}
        """
    )

    _EXPANSION_TEMPLATE = (
        """
        You are a mathematics instructor preparing a **scenario-based multiple-choice question** that requires the integration of multiple mathematical concepts.

        Given the course: {course_name}, chapter: {chapter_name}, and keyword: {keyword}, generate one question that tests the **application of the concept in a real-world or cross-topic scenario**.

        Guidelines:
        - The scenario should require the student to apply at least two different mathematical ideas (e.g., using probability and algebra, or calculus and geometry together).
        - The question should encourage step-by-step reasoning and synthesis of knowledge.
        - Use real-world contexts or problems that naturally require multiple concepts.
        - Provide exactly **1 correct answer** and **3 plausible distractors** based on common student mistakes.
        - Use clear mathematical notation (LaTeX inline: $...$) where appropriate.
        - Include a brief explanation for why the correct answer is right and the others are not.

        Example output structure:
        {{
          "question": "...",
          "choices": {{
            "A": "...",
            "B": "...",
            "C": "...",
            "D": "..."
          }},
          "correct_answer": "A",
          "explanation": "..."
        }}
        """
    )

    @staticmethod
    def multiple_choice_definition_quiz_generation_prompt(course_name: str, chapter_name: str, keyword: str) -> str:
        """
        Returns a prompt for generating a definition-based multiple-choice question that integrates multiple mathematical topics.
        """
        return Math_QuizPrompts._DEFINITION_TEMPLATE.format(
            course_name=course_name,
            chapter_name=chapter_name,
            keyword=keyword,
        )

    @staticmethod
    def multiple_choice_expansion_quiz_generation_prompt(course_name: str, chapter_name: str, keyword: str) -> str:
        """
        Returns a prompt for generating a scenario-based multiple-choice question that integrates multiple mathematical topics.
        """
        return Math_QuizPrompts._EXPANSION_TEMPLATE.format(
            course_name=course_name,
            chapter_name=chapter_name,
            keyword=keyword,
        )
