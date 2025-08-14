from pipeline.science.prompts.zeroshot_flashcards_prompts import ZeroshotPrompts

class Language_ZeroshotPrompts(ZeroshotPrompts):
    @staticmethod
    # Step 2: Chapters generation
    def chapters_generation_prompt():
        """
        Prompt for generating chapters based on the zero-shot topic.
        """
        prompt = \
        """
        You are a great language instructor,
        Here is a language learning topic: {extracted_course_name_domain}
        Generate a list of chapters for learning this topic. Avoid including any methodological chapter topics.
        Make sure to include multiple language families such as Indo-European, Sino-Tibetan, Afro-Asiatic.
        

        Note the "Course name" key should exactly match the topic or a suitably rephrased version.

        Output your response in **valid JSON format only**, using the structure:

        {{
        "Course name": "Your Course Title Here",
        "Chapters": [
            "🗂️ Chapter 1",
            "🧠 Chapter 2",
            ...
        ]
        }}
        """
        return prompt
