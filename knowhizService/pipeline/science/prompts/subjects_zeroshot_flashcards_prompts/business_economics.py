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
        You are a course creator designing content for **Economics** topics, including *Microeconomics* , *Macroeconomics* , *Central Banking* and *financial risk management*.

        - If the topic seems suited for quick learning, create 3–5 chapters.
        - Otherwise, create 7–10 chapters for a more in-depth college-level course.

        Return only a valid **JSON** object like:

        {{
          "Course name": "Your Course Title Here",
          "Chapters": [
            "📘 Chapter 1 Title",
            "📙 Chapter 2 Title",
            ...
          ]
        }}

        **National Income Accounting & Measurement**
        - (★★★) GDP
        - (★★★) GNP
        - (★★★) national income accounting
        - (★★★) real vs nominal GDP
        - (★★★) GDP deflator
        - (★★) consumer price index (CPI)
        - (★★) producer price index (PPI)
        - (★★) net domestic product (NDP)
        - (★★) disposable income
        - (★★) personal income
        - (★) gross national income (GNI)
        - (★) purchasing power parity (PPP)

        **Aggregate Demand & Supply**
        - (★★★) AD-AS
        - (★★★) aggregate demand
        - (★★★) aggregate supply
        - (★★★) short-run aggregate supply (SRAS)
        - (★★★) long-run aggregate supply (LRAS)
        - (★★★) demand-pull inflation
        - (★★★) cost-push inflation
        - (★★) supply shocks
        - (★★) stagflation
        - (★★) recessionary gap
        - (★★) inflationary gap
        - (★) natural rate of output

        **Money & Banking**
        - (★★★) money supply
        - (★★★) money demand
        - (★★★) money multiplier
        - (★★★) fractional reserve banking
        - (★★★) central bank functions
        - (★★★) reserve requirements
        - (★★) discount rate
        - (★★) federal funds rate
        - (★★) open market operations
        - (★★) quantitative easing
        - (★★) velocity of money
        - (★) liquidity trap

        **Economic Models & Theory**
        - (★★★) IS-LM
        - (★★★) IS curve
        - (★★★) LM curve
        - (★★★) Keynesian model
        - (★★★) classical model
        - (★★★) multiplier effect
        - (★★) crowding out
        - (★★) liquidity preference
        - (★★) investment function
        - (★★) consumption function
        - (★★) savings function
        - (★) permanent income hypothesis

        **Fiscal Policy**
        - (★★★) fiscal policy
        - (★★★) government spending
        - (★★★) taxation
        - (★★★) budget deficit
        - (★★★) budget surplus
        - (★★★) automatic stabilizers
        - (★★) discretionary fiscal policy
        - (★★) public debt
        - (★★) debt-to-GDP ratio
        - (★★) fiscal multiplier
        - (★) ricardian equivalence
        - (★) balanced budget multiplier

        **Monetary Policy**
        - (★★★) monetary policy
        - (★★★) inflation targeting
        - (★★★) interest rates
        - (★★★) Taylor rule
        - (★★★) transmission mechanism
        - (★★) expansionary monetary policy
        - (★★) contractionary monetary policy
        - (★★) monetary policy tools
        - (★★) inflation expectations
        - (★★) nominal interest rate
        - (★★) real interest rate
        - (★) zero lower bound

        **Economic Growth & Development**
        - (★★★) economic growth
        - (★★★) productivity growth
        - (★★★) Solow growth model
        - (★★★) technological progress
        - (★★) capital accumulation
        - (★★) human capital
        - (★★) total factor productivity
        - (★★) convergence theory
        - (★★) endogenous growth
        - (★) golden rule of capital
        - (★) steady state

        **International Economics**
        - (★★★) balance of payments
        - (★★★) exchange rates
        - (★★★) trade balance
        - (★★★) current account
        - (★★★) capital account
        - (★★) purchasing power parity
        - (★★) interest rate parity
        - (★★) Marshall-Lerner condition
        - (★★) J-curve effect
        - (★★) Mundell-Fleming model
        - (★) impossible trinity
        - (★) currency crisis

        **Business Cycles & Fluctuations**
        - (★★★) business cycles
        - (★★★) recession
        - (★★★) expansion
        - (★★★) unemployment rate
        - (★★★) natural rate of unemployment
        - (★★★) Phillips curve
        - (★★) cyclical unemployment
        - (★★) structural unemployment
        - (★★) frictional unemployment
        - (★★) output gap
        - (★★) okun's law
        - (★) hysteresis


        **Foundation Theory & Concepts**
        - (★★★) supply & demand
        - (★★★) elasticity
        - (★★★) utility
        - (★★★) market structures
        - (★★★) pricing strategies
        - (★★★) equilibrium price theory
        - (★★★) marginal analysis
        - (★★) opportunity cost
        - (★★) production possibility frontier
        - (★★) market efficiency

        **Consumer Behavior Theory**
        - (★★★) consumer choice theory
        - (★★★) indifference curves
        - (★★★) budget constraint
        - (★★★) income effect
        - (★★★) substitution effect
        - (★★) consumer surplus
        - (★★) revealed preference
        - (★★) Engel curve
        - (★★) Giffen goods
        - (★) network effects
        - (★) behavioral economics

        **Producer Behavior Theory**
        - (★★★) production function
        - (★★★) cost curves
        - (★★★) profit maximization
        - (★★★) marginal cost
        - (★★★) marginal revenue
        - (★★) returns to scale
        - (★★) isoquant curves
        - (★★) producer surplus
        - (★★) economies of scale
        - (★★) economies of scope
        - (★) technical efficiency

        **Market Structure Theory**
        - (★★★) perfect competition
        - (★★★) monopoly
        - (★★★) monopolistic competition
        - (★★★) oligopoly
        - (★★) price discrimination
        - (★★) barriers to entry
        - (★★) market power
        - (★★) Cournot competition
        - (★★) Bertrand competition
        - (★★) game theory
        - (★★) Nash equilibrium
        - (★) contestable markets

        **Factor Market Theory**
        - (★★★) factor markets
        - (★★★) labor market
        - (★★★) capital market
        - (★★) wage determination
        - (★★) rent theory
        - (★★) interest rate theory
        - (★★) marginal productivity theory
        - (★) human capital
        - (★) monopsony

        **Welfare Economics & Policy**
        - (★★★) general equilibrium
        - (★★★) Pareto efficiency
        - (★★★) deadweight loss
        - (★★) welfare economics
        - (★★) market failure
        - (★★) externalities
        - (★★) public goods
        - (★★) asymmetric information
        - (★★) adverse selection
        - (★★) moral hazard
        - (★) mechanism design
        - (★) auction theory

        **Central Bank Origins and Evolution**
        - (★★★) Central Bank Origins and Types
        - (★★★) central bank independence
        - (★★★) central bank governance
        - (★★★) central bank mandates
        - (★★) bank of england model
        - (★★) federal reserve system
        - (★★) european central bank
        - (★★) central bank cooperation
        - (★★) historical development
        - (★★) central bank design
        - (★) central bank accountability
        - (★) central bank transparency

        **Core Functions and Operations**
        - (★★★) Nature and Functions of Central Banks
        - (★★★) lender of last resort
        - (★★★) payment system oversight
        - (★★★) currency issuance
        - (★★★) government banker
        - (★★★) foreign exchange reserves
        - (★★) banknote printing
        - (★★) coin minting
        - (★★) government debt management
        - (★★) financial market operations
        - (★★) clearing and settlement
        - (★) emergency lending facilities

        **Monetary Creation and Control**
        - (★★★) Monetary Creation under Central Bank System
        - (★★★) money supply control
        - (★★★) monetary base
        - (★★★) money multiplier process
        - (★★★) reserve management
        - (★★★) liquidity management
        - (★★) high-powered money
        - (★★) monetary aggregates
        - (★★) credit creation
        - (★★) bank reserves
        - (★★) interbank market
        - (★) monetary transmission

        **Monetary Policy Framework**
        - (★★★) Central Bank Monetary Policy
        - (★★★) inflation targeting
        - (★★★) price stability mandate
        - (★★★) dual mandate
        - (★★★) monetary policy strategy
        - (★★★) policy interest rates
        - (★★) forward guidance
        - (★★) monetary policy communication
        - (★★) policy transmission mechanism
        - (★★) output gap targeting
        - (★★) exchange rate targeting
        - (★) nominal GDP targeting

        **Monetary Policy Tools**
        - (★★★) open market operations
        - (★★★) discount window
        - (★★★) reserve requirements
        - (★★★) interest rate corridor
        - (★★★) standing facilities
        - (★★) repo operations
        - (★★) reverse repo operations
        - (★★) term auction facility
        - (★★) lending facilities
        - (★★) deposit facilities
        - (★★) minimum bid rate
        - (★) marginal lending facility

        **Unconventional Monetary Policy**
        - (★★★) quantitative easing
        - (★★★) asset purchase programs
        - (★★★) negative interest rates
        - (★★★) credit easing
        - (★★) forward guidance
        - (★★) yield curve control
        - (★★) funding for lending
        - (★★) targeted longer-term refinancing
        - (★★) corporate bond purchases
        - (★★) mortgage-backed securities
        - (★) helicopter money
        - (★) modern monetary theory

        **Financial Supervision and Regulation**
        - (★★★) Financial Supervision
        - (★★★) prudential regulation
        - (★★★) bank supervision
        - (★★★) systemic risk monitoring
        - (★★★) macroprudential policy
        - (★★★) financial stability
        - (★★) capital adequacy
        - (★★) stress testing
        - (★★) resolution framework
        - (★★) deposit insurance
        - (★★) banking union
        - (★★) basel accords

        **Crisis Management**
        - (★★★) financial crisis response
        - (★★★) emergency liquidity assistance
        - (★★★) crisis prevention
        - (★★★) too big to fail
        - (★★) bank resolution
        - (★★) deposit guarantee schemes
        - (★★) systemic risk assessment
        - (★★) crisis communication
        - (★★) international coordination
        - (★★) moral hazard
        - (★) bail-in mechanisms
        - (★) living wills

        **International Monetary Relations**
        - (★★★) international monetary system
        - (★★★) exchange rate regimes
        - (★★★) capital flows
        - (★★★) currency swaps
        - (★★) bretton woods system
        - (★★) international reserves
        - (★★) special drawing rights
        - (★★) currency unions
        - (★★) regional monetary cooperation
        - (★★) global financial safety net
        - (★) bancor system
        - (★) tobin tax

        ✦ If it relates to _Foundations of financial risk management_, consider: 
        1. (★★★) Basic concepts of financial risk management
        2. (★★★) Portfolio risk management
        3. (★★★) Advanced risk management
        4. (★★) Financial crisis and financial disasters
        5. (★★) GARP code of conduct
        

        - Generate 7–10 in-depth chapters for undergraduate level courses.
        Do not include any explanation or extra text.

        Topic: {extracted_course_name_domain}
        """

    def flashcards_definition_generation_prompt(self):
        return """
        You are an experienced **Economics** professor writing flashcard definitions for the course **{course_name}**, specifically for chapter **{chapter_name}**.

        Define the keyword: **{keyword}**

        Guidelines:
        - Use **concise academic English** for undergraduates.
        - Refer to *Dornbusch, Fischer & Startz* for macro topics, *Pindyck’s Microeconomics* for micro topics.
        - Emphasize the **core idea** with clear and precise language.
        - If applicable, briefly include a **realistic scenario or use case** to show relevance (e.g., national policy, inflation period, investment cycle).
        - Avoid circular logic (don’t define the term using the term itself).
        - Use **markdown** to highlight critical words (e.g., **GDP**, _price level_).
        - Distinguish between **short-run vs. long-run** if relevant.

        ✦ Incorporate **importance level** into your explanation:
            - (**★★★**) For top-tier terms like **GDP**, **GNP**, **real vs nominal GDP**, definitions should include **practical use**, **policy impact**, and **common misconceptions** (e.g., *confusing GDP with GNP*).
            - (**★★**) For mid-tier terms like **CPI**, **PPI**, **NDP**, relate them to **everyday economic indicators**, price index applications, or common reports (e.g., *how CPI affects wage contracts*).
            - (**★**) For basic-level terms like **GNI** and **PPP**, use **brief examples** (e.g., *comparing income across countries with different currencies*) to build intuition.

        ✦ Common chapter-specific guidance for:
            - _National Income Accounting & Measurement_:
                - Use consistent examples like "calculating GDP in a recession vs. expansion".
                - Highlight distinctions between **nominal vs. real**, and **domestic vs. national** metrics.
                - Clarify how **price indices** (e.g., **GDP deflator**, **CPI**) relate to inflation and purchasing power.


        Output: **only one sentence**, up to {definition_length} words. No prefix or suffix.
        """

    def flashcards_keyword_definition_prompt(self):
        return """
        You are writing **intuitive, accurate, and exam-relevant** definitions of economics keywords, for flashcards used in college-level *Microeconomics* or *Macroeconomics*.

        Keyword: **{keyword}**  
        Chapter: **{chapter_name}**

        Reference guidance:
            - Use **concise academic English** for undergraduates.
            - Refer to *Dornbusch, Fischer & Startz* for macro topics, *Pindyck’s Microeconomics* for micro topics.
            - Emphasize the **core idea** with clear and precise language.
            - If applicable, briefly include a **realistic scenario or use case** to show relevance (e.g., national policy, inflation period, investment cycle).
            - Avoid circular logic (don’t define the term using the term itself).
            - Use **markdown** to highlight critical words (e.g., **GDP**, _price level_).
            - Distinguish between **short-run vs. long-run** if relevant.

            ✦ Incorporate **importance level** into your explanation:
                - (**★★★**) For top-tier terms like **GDP**, **GNP**, **real vs nominal GDP**, definitions should include **practical use**, **policy impact**, and **common misconceptions** (e.g., *confusing GDP with GNP*).
                - (**★★**) For mid-tier terms like **CPI**, **PPI**, **NDP**, relate them to **everyday economic indicators**, price index applications, or common reports (e.g., *how CPI affects wage contracts*).
                - (**★**) For basic-level terms like **GNI** and **PPP**, use **brief examples** (e.g., *comparing income across countries with different currencies*) to build intuition.

            ✦ Common chapter-specific guidance for:
                - _National Income Accounting & Measurement_:
                    - Use consistent examples like "calculating GDP in a recession vs. expansion".
                    - Highlight distinctions between **nominal vs. real**, and **domestic vs. national** metrics.
                    - Clarify how **price indices** (e.g., **GDP deflator**, **CPI**) relate to inflation and purchasing power.


        Please:
        - Write **1 clear sentence**, up to {definition_length} words.
        - Start naturally: “It refers to…”, “This is the idea that…”
        - Use **markdown** to emphasize core terms.
        - Avoid technical symbols, code blocks, and extra formatting.

        Return only the definition sentence.
        """
    
