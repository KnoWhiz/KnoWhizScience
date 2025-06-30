from pipeline.science.prompts.zeroshot_flashcards_prompts import ZeroshotPrompts

class BusinessEconomics_ZeroshotPrompts(ZeroshotPrompts):
    """
    This class is used to generate prompts for the Business Economics domain
    • Business
        • Accounting
        • Finance
        • Marketing
        • Management
        • Business Law
        • Economics (Microeconomics & Macroeconomics merged)
    """

    def chapters_generation_prompt(self):
        return """
        You are a course creator designing content for **Economics** topics, including *Microeconomics* and *Macroeconomics*.

        - If the topic seems suited for quick learning, create 3–5 chapters.
        - Otherwise, create 7–10 chapters for a more in-depth college-level course.

        Return only a valid **JSON** object like:

        {
          "Course name": "Your Course Title Here",
          "Chapters": [
            "📘 Chapter 1 Title",
            "📙 Chapter 2 Title",
            ...
          ]
        }

        ✦ If the course relates to _macroeconomics_, include chapters like: GDP, IS-LM, AD-AS, inflation, monetary policy, etc.
        ✦ If it relates to _microeconomics_, consider: supply & demand, elasticity, utility, market structures, pricing strategies, etc.
        - If the topic is **Central Banking**, refer to the following key modules:
            1. Central Bank Origins and Types
            2. Nature and Functions of Central Banks
            3. Monetary Creation under Central Bank System
            4. Central Bank Monetary Policy
            5. Financial Supervision
        - Generate 7–10 in-depth chapters for undergraduate level courses.
        Do not include any explanation or extra text.

        Topic: {extracted_course_name_domain}
        """

    def flashcards_definition_generation_prompt(self):
        return """
        You are an experienced **Economics** professor writing flashcard definitions for the course **{course_name}**, specifically for chapter **{chapter_name}**.

        Define the keyword: **{keyword}**

        Guidelines:
        - Use **concise academic English**, suitable for undergraduates.
        - Use *Pindyck’s Microeconomics* if the course is micro-oriented.
        - Use *Dornbusch, Fischer & Startz* if the course is macro-oriented.
        - Focus on the **core idea** — avoid long explanations or examples.
        - Use **markdown** for key terms (**bold** or _italic_).
        - Avoid circular logic or copying the keyword.
        - Clarify short-run vs long-run if applicable.
        - If the topic is **Central Banking**, refer to the following key modules:
            - Origins and development of central banks (e.g., Sweden, England, U.S. Fed)
            - Key functions: Issuer of currency, Bankers' bank, Government’s bank
            - Types of systems: Single, dual, quasi, transnational
            - Organizational structure and branch reforms (e.g., China’s PBoC reform of 1998)
            - Central bank's independence and constraints
            - Tools of monetary policy (reserve ratio, open market, rediscount, SLF/MLF/PSL)
            - Effects and goals of monetary policy (inflation, employment, balance of payments)
            - Financial supervision and Basel standards

        Output: **only one sentence**, up to {definition_length} words. No prefix or suffix.
        """

    def flashcards_keyword_definition_prompt(self):
        return """
        You are writing **intuitive, accurate, and exam-relevant** definitions of economics keywords, for flashcards used in college-level *Microeconomics* or *Macroeconomics*.

        Keyword: **{keyword}**  
        Chapter: **{chapter_name}**

        Reference guidance:
        - _Pindyck's Microeconomics_ → supply/demand, elasticity, utility, game theory, cost curves, etc.
        - _Dornbusch et al._ → GDP, IS-LM, inflation, unemployment, fiscal/monetary policy, etc.
        - If the topic is **Central Banking**, refer to the following key modules:
            - Central bank roles: currency issuance, lender of last resort, clearinghouse
            - Institutions: People's Bank of China, U.S. Federal Reserve, ECB, etc.
            - Instruments: Required reserve ratio, open market operations, rediscount rate
            - Modern tools: SLF, MLF, PSL, TMLF, repo, reverse repo
            - Organizational elements: Monetary Policy Committee, statistical and audit departments
            - Regulatory functions: anti-money laundering, capital adequacy (CAMELS), Basel norms
            - Transmission mechanisms: from monetary base to total money supply (MB → M)

        Please:
        - Write **1 clear sentence**, up to {definition_length} words.
        - Start naturally: “It refers to…”, “This is the idea that…”
        - Use **markdown** to emphasize core terms.
        - Avoid technical symbols, code blocks, and extra formatting.

        Return only the definition sentence.
        """
    
