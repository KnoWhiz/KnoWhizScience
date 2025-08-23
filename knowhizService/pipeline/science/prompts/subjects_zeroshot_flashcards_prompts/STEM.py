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
    # Step 2: Chapters generation
    def chapters_generation_prompt():
        """
        Prompt for generating chapters based on the zero-shot topic.
        """
        prompt = \
        """
        You are a great STEM instructor specializing in Physics,
        Here is a STEM learning topic: {extracted_course_name_domain}
        Generate a list of chapters for learning this topic. Focus on fundamental concepts and practical applications.
        Make sure to include multiple physics branches and not just one.
        
        Note the "Course name" key should exactly match the topic or a suitably rephrased version.

        Output your response in **valid JSON format only**, using the structure:

        {{
        "Course name": "Your Course Title Here",
        "Chapters": [
            "🔬 Chapter 1",
            "⚡ Chapter 2",
            "🧪 Chapter 3",
            "📐 Chapter 4",
            "⚖️ Chapter 5",
            "🔄 Chapter 6",
            "🌌 Chapter 7",
            "📊 Chapter 8"
        ]
        }}
        """
        return prompt

    @staticmethod
    # Step 3: Keywords generation for each chapter
    def keywords_generation_prompt():
        """
        Prompt for generating keywords for each chapter.
        """
        prompt = \
        """
        You are a great STEM instructor specializing in Physics,
        Generate keywords for the chapter: {chapter_name} in the course: {course_name}.
        Focus on fundamental physics concepts, laws, formulas, and practical applications.
        
        Output your response in **valid JSON format only**, using the structure:

        {{
        "keywords": [
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
            }}
        ]
        }}
        """
        return prompt

    @staticmethod
    # Step 4: Flashcards definition generation
    def flashcards_definition_generation_prompt():
        """
        Prompt for generating flashcards definitions.
        """
        prompt = \
        """
        You are a great STEM instructor specializing in Physics,
        Create a precise definition for the keyword: {keyword} in the context of {course_name}, chapter: {chapter_name}.
        
        **Requirements:**
        1. Use precise physics terminology and correct mathematical notation
        2. Include essential components, units, and relationships
        3. Use proper LaTeX notation for formulas: $E = mc^2$ for inline, $$F = ma$$ for display
        4. Maximum 150 words
        5. Use bold formatting for key terms
        
        Output your response in **valid Markdown format only**.
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
        1. The section name is 'Examples', which only includes real-world examples to help memorize and understand the keyword in {course_name}.
        2. Please do not provide the definition of the keyword in the example.
        3. Within each example, provide a clear step-by-step breakdown to enhance memorization and understanding of the concept.
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
