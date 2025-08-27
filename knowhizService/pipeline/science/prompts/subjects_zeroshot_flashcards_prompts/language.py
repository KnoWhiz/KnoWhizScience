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
        You are a skilled language instructor.
        The student wants to learn the following language: {extracted_course_name_domain}

        Generate a structured course with chapters specifically designed for learning this language. 
        If the language is French, Japanese, Mandarin, Spanish, or Standard Arabic (Modern Standard Arabic),
        make the content tailored directly to that language’s script, phonology, grammar, vocabulary, and culture.
        If it is another language, still generate a language-appropriate course.

        Each chapter should represent a major step in language learning (alphabet/characters, basic pronunciation,
        core grammar, key phrases, conversation skills, listening/reading practice, cultural context, advanced vocabulary, etc.).

        Ensure at least one flashcard per chapter compares a sentence in the target language with its English equivalent. 
        Examples: 
        - French: "Je mange une pomme." ↔ "I am eating an apple."
        - Japanese: "私はリンゴを食べます。" ↔ "I eat an apple."
        - Mandarin: "我在吃苹果。" ↔ "I am eating an apple."
        - Spanish: "Estoy comiendo una manzana." ↔ "I am eating an apple."
        - Standard Arabic (MSA): "أنا آكل تفاحة." ↔ "I am eating an apple."

        For Japanese and Mandarin, include script-specific guidance (kana/kanji for Japanese; characters, pinyin, and tones for Mandarin).
        For Standard Arabic, include Arabic script, basic orthography/diacritics, root-and-pattern morphology, and MSA-focused grammar.
        For Spanish, emphasize verb conjugations (present, preterite, imperfect), gender/number agreement, and common idioms.

        Output your response in **valid JSON format only**, using this structure:

        {
          "Course name": "Your Course Title Here",
          "Chapters": [
            "🗂️ Chapter 1: ...",
            "🧠 Chapter 2: ...",
            "🗣️ Chapter 3: ...",
            "📚 Chapter 4: ...",
            "🛫 Chapter 5: ..."
          ]
        }
        """
        return prompt
