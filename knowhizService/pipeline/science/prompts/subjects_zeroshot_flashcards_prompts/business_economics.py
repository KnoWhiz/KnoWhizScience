from pipeline.science.prompts.zeroshot_flashcards_prompts import ZeroshotPrompts

class BusinessEconomics_ZeroshotPrompts(ZeroshotPrompts):
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
    def chapters_generation_prompt(self):
        course_text = self.course_name_domain.get("text", "").lower()

        if "macroeconomics" in course_text or "macro" in course_text:
            return self.Macro.chapters_generation_prompt()
        elif "microeconomics" in course_text or "micro" in course_text:
            return self.Micro.chapters_generation_prompt()
        else:
            return super().chapters_generation_prompt()

    class Macro:
        @staticmethod
        def chapters_generation_prompt():
            return """
            You are a course creator. I will provide a topic, but **no explicit coverage type**. You must determine whether the topic should be treated as "quick learn" (or marked as "pre-college level") or a more in-depth course:

            - If, from context, you believe the topic is for quick and easy learning, create 3–5 chapters.
            - Otherwise, create 7–10 chapters like a more in-depth course in college.

            Output your response in **valid JSON format only**, using the structure:

            {{
            "Course name": "Your Course Title Here",
            "Chapters": [
                "Chapter 1",
                "Chapter 2",
                ...
            ]
            }}

            Ensure:
            1. The "Course name" key exactly matches the topic or a suitably rephrased version.
            2. The "Chapters" key contains an appropriate list of chapter titles based on your inferred coverage type (3–5 if "quick learn", 7–10 if in-depth).
            3. Each chapter starts with a suitable emoji as examples below.
            4. Provide no additional text or explanation—only the JSON.

            --- Example of the desired output for a college-level economics course:

            ```json
            {{
            "Course name": "Macroeconomics",
            "Chapters": [
                "Fundamental Concepts and Indicators",
                "Macroeconomic Models: IS-LM and AD-AS",
                "Unemployment and Inflation",
                "Fiscal and Monetary Policy",
                "Economic Growth and Business Cycles",
                "Open Economy and Exchange Rate Systems",
                "Policy Debates and Economic Schools of Thought",
                "Diagram and Model Analysis Training"
            ]
            }}
            ```

            Now, here is my topic: {extracted_course_name_domain}
            """
        @staticmethod
        def flashcards_definition_generation_prompt():
            prompt = \
            """
            You are an economics instructor generating flashcard definitions for the course **{course_name}**, specifically for chapter **{chapter_name}**.

            Define the keyword: **{keyword}** clearly and precisely.

            Your definition must follow these guidelines:

            1. Use **concise, academic English**, suitable for undergraduates studying macroeconomics.
            2. Ensure the explanation matches the standard textbook definition — especially aligned with *Dornbusch, Fischer, and Startz: Macroeconomics (13th edition)*.
            3. Include only the **core idea** — avoid extra examples or long explanations.
            4. Avoid circular logic or rephrasing the keyword as its own definition.
            5. Format key economic terms in **bold** or _italics_ using Markdown.
            6. If applicable, clarify short-run vs long-run context or exam-relevant interpretations.

            Output only the **definition sentence**, no preamble, no explanation.

            Maximum words: {definition_length}
            """
            return prompt
        
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
        def flashcards_definition_generation_prompt():
            prompt = """
            You are an experienced professor of **Microeconomics**, preparing precise and accessible flashcard definitions for undergraduate students. These definitions are based on the style and content of _Pindyck's Microeconomics_, with reference to the following key chapter insights:

             **Reference Chapter Highlights**:

            1. **Introduction**:
            - Scarcity and choice; market vs. non-market environments
            - Nominal vs real prices; marginal vs total analysis

            2. **Supply and Demand**:
            - Law of demand/supply; market equilibrium
            - Elasticity: price, income, and cross-price
            - Short-run vs long-run elasticity

            3. **Consumer Behavior**:
            - Cardinal vs ordinal utility; indifference curves
            - Budget constraint, consumer choice, and surplus
            - Substitution/income effect; revealed preference

            4. **Production Theory**:
            - Production function; diminishing returns
            - Isoquants, MRTS, returns to scale

            5. **Cost Theory**:
            - Short-run vs long-run cost curves
            - Economies of scope; learning curves

            6. **Perfect Competition**:
            - MR = MC; short-run vs long-run equilibrium
            - Producer surplus and allocative efficiency

            7. **Monopoly and Monopsony**:
            - Pricing with market power
            - Deadweight loss; antitrust implications

            8. **Pricing Strategies**:
            - Price discrimination (1st, 2nd, 3rd degree)
            - Two-part tariffs, bundling, peak-load pricing

            9. **Monopolistic and Oligopolistic Markets**:
            - Product differentiation
            - Cournot, Bertrand, Stackelberg models

            10. **Game Theory**:
                - Dominant strategy, Nash equilibrium
                - Repeated games, threats, and commitment

            11. **Factor Markets**:
                - Labor, land, and capital pricing
                - Marginal productivity and monopsony

            12. **General Equilibrium & Welfare**:
                - Pareto efficiency, Edgeworth box
                - Trade benefits, market completeness

            13. **Market Failure & Policy**:
                - Externalities, public goods
                - Asymmetric information; government intervention

            ---

             Now, for the keyword: **"{keyword}"**, from chapter **"{chapter_name}"**, write a **one-sentence definition** that:

            - Is simple, conceptually accurate, and accessible.
            - Begins naturally: _“It refers to…”_, _“This is the idea that…”_, etc.
            - Avoids formulas and jargon unless necessary.
            - Uses **markdown** to bold or italicize important terms (but no backticks).
            - Is maximum {definition_length} words.
            - **Do not** add any prefix/suffix or code block markers.

             Output only the definition sentence.
            """
            return prompt
        
        @staticmethod
        def flashcards_keyword_definition_prompt():
            prompt = """
        You are an experienced professor writing **concise, intuitive, and accurate definitions** of core concepts in *Microeconomics*, for students using Pindyck's textbook.

        Use the following chapter-wise background as reference when writing each definition. Always assume the student has read the textbook but needs a clear reminder.

        **Reference Chapter Highlights**:

        1. **Introduction**:
        - Scarcity vs. choice; what is a market; nominal vs real price; marginal reasoning

        2. **Supply and Demand**:
        - Laws of supply/demand, price elasticity, market equilibrium, determinants of shifts

        3. **Consumer Behavior**:
        - Marginal utility, indifference curves, budget constraint, income/substitution effects

        4. **Production Theory**:
        - Production function, diminishing returns, MRTS, returns to scale

        5. **Cost Theory**:
        - Short-run vs long-run costs, MC, AC, economies of scale/scope

        6. **Perfect Competition**:
        - MR=MC, entry/exit, efficiency, producer surplus

        7. **Monopoly and Monopsony**:
        - Market power, price setting, deadweight loss, regulation

        8. **Pricing Strategies with Market Power**:
        - Price discrimination, bundling, two-part tariffs, advertising

        9. **Monopolistic Competition and Oligopoly**:
        - Product differentiation, Cournot vs Bertrand vs Stackelberg, collusion

        10. **Game Theory**:
            - Nash equilibrium, dominant strategies, repeated games, strategic moves

        11. **Factor Markets**:
            - Derived demand, marginal productivity theory, monopsony

        12. **General Equilibrium & Welfare**:
            - Pareto efficiency, Edgeworth box, competitive markets’ efficiency

        13. **Market Failures & Policy**:
            - Externalities, public goods, asymmetric info, government intervention

        ---

        Now, for the **keyword**: "{keyword}" (from chapter: "{chapter_name}"), please:

        - Write a **1-sentence definition**, up to {definition_length} words
        - Start naturally (e.g., “It refers to…”, “This is the idea that…”)
        - Use **markdown** to bold or _italicize_ important terms
        - Be **precise, intuitive**, and aligned with undergraduate logic
        - Avoid formulas, jargon, and technical language unless essential
        - Do **not** include extra formatting like triple backticks or titles

        Only return the definition sentence, nothing else.
        """
            return prompt
        
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