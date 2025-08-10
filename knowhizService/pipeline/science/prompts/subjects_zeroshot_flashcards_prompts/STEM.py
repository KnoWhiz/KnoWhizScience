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
    # Step 2: Chapters generation - STEM-specific
    def chapters_generation_prompt():
        """
        Prompt for generating chapters based on the zero-shot topic, specifically tailored for STEM subjects with focus on Physics.
        """
        prompt = \
        """
        You are a STEM course creator specializing in Science, Technology, Engineering, and Mathematics with particular expertise in Physics. 
        I will provide a topic, and you must determine the appropriate depth and structure:

        **STEM Course Structure Guidelines:**
        - **Quick Learn/Pre-college**: 3-5 chapters with fundamental concepts
        - **In-depth/College-level**: 7-10 chapters with comprehensive coverage
        - **Advanced/Research-level**: 10-15 chapters with specialized topics

        **STEM-Specific Considerations:**
        1. **Physics**: Include theoretical foundations, mathematical formulations, experimental methods, and real-world applications
        2. **Chemistry**: Structure around molecular interactions, reaction mechanisms, and laboratory techniques
        3. **Biology**: Structure around biological systems, processes, and experimental methods
        4. **Mathematics**: Build from fundamentals to advanced applications with rigorous proofs
        5. **Engineering**: Include design principles, analysis methods, and practical implementation

        Output your response in **valid JSON format only**:

        {{
        "Course name": "Your STEM Course Title",
        "Chapters": [
            "🔬 Chapter 1: Foundation",
            "⚡ Chapter 2: Core Concepts",
            "🧪 Chapter 3: Applications",
            ...
        ],
        "STEM_Domain": "Physics|Chemistry|Biology|Mathematics|Engineering|Mixed",
        "Difficulty_Level": "Beginner|Intermediate|Advanced"
        }}

        **STEM Chapter Naming Conventions:**
        - Use relevant STEM emojis: 🔬🧪⚡🌱📊⚙️🔧🧮🌌
        - Include clear progression indicators
        - Emphasize practical applications where appropriate

        Example for Physics:
        ```json
        {{
        "Course name": "Classical Mechanics",
        "Chapters": [
            "🔬 Fundamental Concepts and Units",
            "⚡ Newton's Laws of Motion",
            "📐 Kinematics and Vector Analysis",
            "⚖️ Dynamics and Force Analysis",
            "🔄 Energy, Work, and Power",
            "🌌 Gravitation and Central Forces",
            "🔄 Rotational Motion and Angular Momentum",
            "📊 Oscillations and Simple Harmonic Motion",
            "🌊 Wave Motion and Sound"
        ],
        "STEM_Domain": "Physics",
        "Difficulty_Level": "Intermediate"
        }}
        ```

        Example for Chemistry:
        ```json
        {{
        "Course name": "Physical Chemistry",
        "Chapters": [
            "🧪 Atomic Structure and Quantum Theory",
            "⚛️ Chemical Bonding and Molecular Structure",
            "🌡️ Thermodynamics and Energy",
            "⚡ Kinetics and Reaction Rates",
            "⚖️ Chemical Equilibrium",
            "🔬 Spectroscopy and Molecular Properties",
            "🌊 Surface Chemistry and Catalysis"
        ],
        "STEM_Domain": "Chemistry",
        "Difficulty_Level": "Advanced"
        }}
        ```
        """
        return prompt

    @staticmethod
    # Step 3: Keywords generation for each chapter - STEM-specific
    def keywords_generation_prompt():
        """
        Prompt for generating keywords for each chapter, specifically tailored for STEM subjects with focus on Physics.
        """
        prompt = \
        """
        You are a STEM education expert with deep knowledge of Physics. Generate keywords for the chapter: {chapter_name} in the course: {course_name}.

        **STEM-Specific Keyword Requirements:**
        1. **Core Concepts**: Include fundamental principles, laws, and theories
        2. **Mathematical Notation**: Include key formulas, equations, and mathematical relationships
        3. **Practical Applications**: Include real-world applications and experimental methods
        4. **Experimental Methods**: Include laboratory techniques, measurements, and procedures
        5. **Problem-Solving Tools**: Include analytical methods, computational techniques, and visualization tools

        **Keyword Categories by STEM Domain:**
        - **Physics**: Laws, principles, formulas, units, experimental methods, mathematical relationships
        - **Chemistry**: Reactions, compounds, mechanisms, laboratory techniques, molecular structures
        - **Biology**: Processes, systems, organisms, experimental methods, biological structures
        - **Mathematics**: Theorems, formulas, methods, proofs, applications, computational techniques
        - **Engineering**: Design principles, analysis methods, materials, systems, optimization techniques

        **Output Format:**
        Return a JSON array of keywords, each with:
        - **keyword**: The term or concept
        - **category**: "Law", "Formula", "Method", "Application", "Theory", "Principle", "Technique"
        - **importance**: "High", "Medium", "Low" based on chapter centrality

        Example output for Physics:
        ```json
        [
            {{
                "keyword": "Newton's Second Law",
                "category": "Law",
                "importance": "High"
            }},
            {{
                "keyword": "F = ma",
                "category": "Formula",
                "importance": "High"
            }},
            {{
                "keyword": "Free Body Diagram",
                "category": "Method",
                "importance": "Medium"
            }},
            {{
                "keyword": "Vector Addition",
                "category": "Technique",
                "importance": "Medium"
            }}
        ]
        ```

        **Guidelines:**
        1. Generate 8-15 keywords per chapter
        2. Prioritize concepts that build upon each other
        3. Include both theoretical and practical aspects
        4. Use precise scientific terminology
        5. Consider prerequisite knowledge and learning progression
        6. For Physics, emphasize mathematical relationships and experimental verification
        """
        return prompt

    @staticmethod
    # Step 4: Flashcards definition generation - STEM-specific
    def flashcards_definition_generation_prompt():
        """
        Prompt for generating flashcards definitions, specifically tailored for STEM subjects with focus on Physics.
        """
        prompt = \
        """
        You are a STEM education expert with specialization in Physics. Create a precise, comprehensive definition for the keyword: {keyword} in the context of {course_name}, chapter: {chapter_name}.

        **STEM Definition Requirements:**
        1. **Accuracy**: Use precise scientific terminology and correct mathematical notation
        2. **Completeness**: Include essential components, units, and relationships
        3. **Clarity**: Explain complex concepts in accessible language
        4. **Context**: Relate to the broader field and chapter topic
        5. **Mathematical Precision**: Use proper LaTeX notation for formulas

        **Definition Structure:**
        - **Core Definition**: Primary explanation of the concept
        - **Key Components**: Essential elements or variables
        - **Mathematical Expression**: If applicable, include formulas in LaTeX
        - **Units**: Specify units of measurement where relevant
        - **Context**: Brief connection to broader STEM principles

        **STEM-Specific Guidelines:**
        - **Physics**: Include units, vector notation, reference frames, and experimental verification
        - **Chemistry**: Include molecular structures, reaction mechanisms, and conditions
        - **Biology**: Include biological systems, processes, and experimental contexts
        - **Mathematics**: Include formal definitions, theorems, and proofs
        - **Engineering**: Include design principles, materials, and applications

        **LaTeX Formula Guidelines:**
        - Use proper mathematical notation: $E = mc^2$ for inline, $$F = ma$$ for display
        - Include vector notation: $\\vec{F}$ for vectors
        - Use subscripts and superscripts: $v_0$, $a^2$
        - Include units: $F = 5.0 \\text{ N}$
        - Use proper physics notation: $\\Delta x$, $\\frac{d}{dt}$

        **Example Definition Format for Physics:**
        ```
        **Newton's Second Law**: A fundamental principle stating that the acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass. Mathematically expressed as $\\vec{F} = m\\vec{a}$, where $\\vec{F}$ is the net force (in newtons, N), $m$ is the mass (in kilograms, kg), and $\\vec{a}$ is the acceleration (in meters per second squared, m/s²). This law forms the foundation of classical mechanics and is essential for understanding motion and dynamics in inertial reference frames.
        ```

        **Requirements:**
        1. Maximum 150 words for the complete definition
        2. Use bold formatting for key terms
        3. Include mathematical expressions in LaTeX when applicable
        4. Maintain scientific accuracy and precision
        5. Connect to broader STEM principles and applications
        6. For Physics, emphasize mathematical relationships and experimental verification
        """
        return prompt

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

    @staticmethod
    # Step 5: Flashcards expansion generation - Advanced STEM version
    def flashcards_expansion_generation_prompt_advanced():
        """
        Advanced prompt for generating flashcards expansions with deeper STEM analysis, specialized for Physics.
        """
        prompt = \
        """
        You are a senior STEM researcher and educator with expertise in Physics. Create a comprehensive expansion for the keyword: {keyword} in {course_name}, chapter: {chapter_name}.
        
        **Definition**: {definition}
        
        **Advanced STEM Expansion Requirements:**
        
        **1. Theoretical Foundation (30% of content):**
        - Mathematical derivation or theoretical basis
        - Fundamental principles and assumptions
        - Historical context and development
        - Connection to broader physical laws
        
        **2. Practical Applications (40% of content):**
        - Real-world examples and case studies
        - Laboratory procedures or experimental methods
        - Industrial or research applications
        - Engineering implementations
        
        **3. Problem-Solving Framework (20% of content):**
        - Step-by-step solution methodology
        - Common pitfalls and error analysis
        - Optimization strategies and best practices
        - Computational approaches when applicable
        
        **4. Advanced Connections (10% of content):**
        - Links to related concepts and theories
        - Current research developments
        - Future applications and implications
        - Cross-disciplinary connections
        
        **STEM-Specific Advanced Guidelines:**
        
        **Physics Advanced:**
        - Include relativistic or quantum corrections when applicable
        - Discuss experimental verification and precision measurements
        - Connect to fundamental forces and conservation laws
        - Emphasize mathematical rigor and physical interpretation
        - Include computational physics methods when relevant
        
        **Chemistry Advanced:**
        - Include reaction mechanisms and kinetics
        - Discuss thermodynamic considerations
        - Connect to molecular orbital theory and quantum chemistry
        - Emphasize experimental design and data analysis
        
        **Biology Advanced:**
        - Include molecular mechanisms and cellular processes
        - Discuss evolutionary context and ecological implications
        - Connect to systems biology and network analysis
        - Emphasize experimental design and statistical analysis
        
        **Mathematics Advanced:**
        - Include rigorous proofs and formal definitions
        - Discuss computational complexity and numerical methods
        - Connect to abstract algebra and topology
        - Emphasize logical reasoning and mathematical beauty
        
        **Engineering Advanced:**
        - Include finite element analysis and computational modeling
        - Discuss optimization and design trade-offs
        - Connect to systems engineering and control theory
        - Emphasize practical implementation and real-world constraints
        
        **Formatting Requirements:**
        - Use LaTeX for all mathematical expressions
        - Include tables for data comparison
        - Use diagrams for complex processes
        - Maximum {expansion_length} words
        - Proper markdown formatting throughout
        """
        return prompt
