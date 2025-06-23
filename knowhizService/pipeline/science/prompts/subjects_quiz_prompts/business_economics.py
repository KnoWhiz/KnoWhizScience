from pipeline.science.prompts.quiz_prompts import QuizPrompts

class BusinessEconomics_QuizPrompts(QuizPrompts):
    """
    This class is used to generate prompts for the Business Economics domain
    •	Business
        •	Accounting
        •	Finance
        •	Marketing
        •	Management
        •	Business Law
	•	Economics
        •	Microeconomics
        •	Macroeconomics
    """
    def get_subject_prompt_class(self):
        course_text = self.course_name_domain.get("text", "").lower()
        if "macroeconomics" in course_text or "macro" in course_text:
            return self.Macro
        elif "microeconomics" in course_text or "micro" in course_text:
            return self.Micro
        else:
            return super()

    def multiple_choice_definition_quiz_generation_prompt(self):
        subject_cls = self.get_subject_prompt_class()
        return subject_cls.multiple_choice_definition_quiz_generation_prompt()

    def multiple_choice_expansion_quiz_generation_prompt(self):
        subject_cls = self.get_subject_prompt_class()
        return subject_cls.multiple_choice_expansion_quiz_generation_prompt()

    def chapter_quiz_generation_prompt(self):
        subject_cls = self.get_subject_prompt_class()
        return subject_cls.chapter_quiz_generation_prompt()


    class Macro:
        
        @staticmethod
        def multiple_choice_definition_quiz_generation_prompt():
            prompt = \
            """
            You are a macroeconomics instructor designing multiple-choice questions for undergraduate students.

            Given the course: {course_name}, chapter: {chapter_name}, and concept: {keyword}, generate a well-structured multiple-choice question that assesses the student's **understanding of the term’s definition**.

            Requirements:
            1. Use a formal, exam-oriented tone based on standard textbooks (e.g., Dornbusch Macroeconomics or Gaokao-style summaries).
            2. The question stem should begin with verbs like *Which of the following best defines...* or *What is the correct description of...*
            3. Generate **one correct answer** and **three plausible distractors** that reflect typical student misunderstandings (e.g., mixing up GDP and GNP).
            4. Distractors must be grammatically correct and not obviously wrong.
            5. Format output using the JSON structure:

            ```json
            {{
            "question": "...",
            "options": ["A...", "B...", "C...", "D..."],
            "answer": "B",
            "explanation": "Explain briefly why B is correct and others are wrong."
            }}
            ```

            Only output the JSON. Avoid footnotes or commentary.
            """
            return prompt
        @staticmethod
        def multiple_choice_expansion_quiz_generation_prompt():
            prompt = \
            """
            You are a macroeconomics instructor preparing scenario-based multiple-choice questions.

            Given the course: {course_name}, chapter: {chapter_name}, and keyword: {keyword}, create a multiple-choice question that **applies this concept to a real-world or policy scenario**.

            Guidelines:
            1. Frame the question based on macroeconomic models (e.g., IS-LM, AD-AS, Phillips Curve, etc.) or real policy actions (e.g., interest rate changes, taxation).
            2. The stem should reflect exam language such as: *If the government increases spending...*, or *Under a fixed exchange rate system...*
            3. Include **one correct answer** and **three realistic distractors** based on common confusion (e.g., short-run vs. long-run, inflation expectations, crowding-out).
            4. Ensure options are mutually exclusive and conceptually clear.
            5. Format output as valid JSON:

            ```json
            {{
            "question": "...",
            "options": ["A...", "B...", "C...", "D..."],
            "answer": "C",
            "explanation": "Explain the economic reasoning behind the correct choice."
            }}
            ```

            Provide only the JSON result. No additional text.
            """
            return prompt




    class Micro:
        
        @staticmethod
        def chapter_quiz_generation_prompt():
            prompt = """
        You are an experienced economics instructor preparing a set of **quiz questions** for a university-level course based on *Pindyck's Microeconomics* textbook.

        Focus on the following chapter: "{chapter_name}".

        Please generate {num_questions} quiz questions that:
        - Match the core concepts of the chapter
        - Reflect the **style and depth** of undergraduate economics exams
        - Are written clearly, with no ambiguity or overly complex language
        - Vary in type (MCQ, True/False, Fill-in-the-blank), but all must be conceptually grounded
        - Each question should target **one key idea or potential misconception**

        Examples of key concept types include:
        - Definitions (e.g., marginal cost, elasticity, Nash equilibrium)
        - Graphical intuition (e.g., shape of indifference curve)
        - Logical reasoning (e.g., "If X increases, what happens to Y?")
        - Formula application (but no algebra-heavy math)

        Instructions:
        - Write each question followed by 4 answer choices (A–D), and indicate the correct one with "Answer: X"
        - Avoid trick questions; instead, focus on **frequently misunderstood** or subtle points
        - Use Markdown format (no code blocks), and bold the **correct answer** in explanations

        Base the content on the following chapter insights:

        """
            # You can dynamically insert the chapter highlights here (e.g., from Microeconomics Chapter 4)
            return prompt

    pass