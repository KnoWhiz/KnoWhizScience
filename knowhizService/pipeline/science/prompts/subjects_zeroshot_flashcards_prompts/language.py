from pipeline.science.prompts.zeroshot_flashcards_prompts import ZeroshotPrompts

class Language_ZeroshotPrompts(ZeroshotPrompts):
    @staticmethod
    # Step 2: Chapters generation
    def chapters_generation_prompt():
        """
        Prompt for generating vocabulary-based chapters for a language learning topic.
        """
        return (
            "You are a skilled language instructor. "
            "Given the learning topic '{extracted_course_name_domain}', generate engaging chapters. "
            "Each chapter should focus on a coherent group of words or phrases by usage scenario, grammatical property, or thematic set (e.g., greetings, travel vocabulary, past-tense verbs). "
            "Do NOT include methodology, teaching strategies, or meta-topics—only content clusters."
            "\n\n"
            "Ensure the JSON 'Course name' matches or suitably rephrases the topic. "
            "Output ONLY valid JSON with this exact structure:\n"
            "{\n"
            "  \"Course name\": \"<Course Title>\",\n"
            "  \"Chapters\": [\n"
            "    \"Chapter 1: <Title>\",\n"
            "    \"Chapter 2: <Title>\",\n"
            "    ...\n"
            "  ]\n"
            "}\n"
        )
