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
        Prompt for generating flashcards expansions for each keyword.
        """
        prompt = \
        """
        You are a great STEM instructor specializing in Physics,
        For the course: {course_name}, chapter: {chapter_name}, provide examples for the keyword: {keyword}.
        {keyword}'s definition is: {definition}.
        
        **Requirements:**
        1. Include at least two different worked examples using LaTeX for physics notation
        2. Add a 'Common Mistake' section explaining typical errors
        3. Use proper markdown formatting
        4. Maximum {expansion_length} words
        5. Focus on fundamental physics principles and real-world applications
        
        Output your response in **valid Markdown format only**.
        """
        return prompt
