from pipeline.science.prompts.quiz_prompts import QuizPrompts

class BusinessEconomics_QuizPrompts(QuizPrompts):
    """
    Prompt generator for Business Economics quizzes.
    Covers Microeconomics, Macroeconomics, and Central Banking under unified logic.
    """

    def multiple_choice_definition_quiz_generation_prompt(self):
        return """
        You are a university-level Economics instructor creating **definition-based multiple-choice questions**.

        Given the course: {course_name}, chapter: {chapter_name}, and concept: {keyword}, generate one question that tests the student's understanding of the **term’s definition**.

        ✦ If the topic is *Microeconomics*, include terms like:
          - supply & demand, elasticity, utility, cost curves, market structures, Nash equilibrium

        ✦ If the topic is *Macroeconomics*, focus on:
          - GDP, IS-LM, AD-AS, inflation, fiscal/monetary policy, unemployment, multiplier effect

        ✦ If the topic is *Central Banking*, refer to:
          - Central bank functions (currency issuance, lender of last resort)
          - Tools (reserve ratio, open market operations, rediscount rate, MLF/SLF/PSL)
          - Institutional features (PBoC, Federal Reserve, ECB)
          - Monetary policy goals: inflation, employment, exchange rates, stability

        Requirements:
        - Use an exam-oriented tone, based on textbooks like *Pindyck*, *Dornbusch*, or standard central banking references
        - Start the question with: *Which of the following best defines...* or *What is the correct explanation of...*
        - Provide exactly **1 correct answer** and **3 plausible distractors** based on common student confusion

        Format the output as JSON:

        ```json
        {{
          "question": "...",
          "options": ["A...", "B...", "C...", "D..."],
          "answer": "C",
          "explanation": "Explain briefly why C is correct and others are not"
        }}
        ```

        Output only the JSON.
        """

    def multiple_choice_expansion_quiz_generation_prompt(self):
        return """
        You are an Economics instructor preparing **scenario-based multiple-choice questions**.

        Given the course: {course_name}, chapter: {chapter_name}, and keyword: {keyword}, generate one question that tests the **application of the concept in a real-world or policy scenario**.

        ✦ If it's *Microeconomics*, consider:
          - Firm behavior, pricing strategies, consumer decisions, externalities

        ✦ For *Macroeconomics*, frame using:
          - Policy shocks, IS-LM, AD-AS, Phillips Curve, output gap, interest rates

        ✦ For *Central Banking*, use:
          - Reactions to inflation/deflation
          - Use of interest rate tools or liquidity management
          - Transmission of monetary policy into the real economy

        Guidelines:
        - The question stem should be realistic and policy-grounded: e.g., *If the central bank raises interest rates...*
        - Include **1 correct answer** and **3 distractors** based on common student mistakes
        - Ensure all options are clear, mutually exclusive, and plausible

        Format in JSON:

        ```json
        {{
          "question": "...",
          "options": ["A...", "B...", "C...", "D..."],
          "answer": "A",
          "explanation": "Why this option is correct given the scenario"
        }}
        ```

        Output only the JSON.
        """

    def chapter_quiz_generation_prompt(self):
        return """
        You are an experienced instructor writing **chapter-based quiz questions** for an undergraduate Economics course.

        Focus on this chapter: {chapter_name}. Generate {num_questions} questions.

        Your content may involve:
        ✦ *Microeconomics*: supply/demand, cost structure, market behavior, welfare, consumer theory, game theory  
        ✦ *Macroeconomics*: output determination, fiscal/monetary policy, inflation, unemployment, economic growth  
        ✦ *Central Banking*: bank roles, policy tools, monetary transmission, institutional frameworks, Basel regulations

        Instructions:
        - Use mixed formats (MCQ, True/False, Fill-in-the-blank)
        - Each question should test **one important concept or common student confusion**
        - Avoid trick questions; focus on clarity and conceptual depth
        - Use Markdown format. Indicate answers clearly like:  
          `Answer: B`

        Do not include commentary or explanations unless asked.
        """