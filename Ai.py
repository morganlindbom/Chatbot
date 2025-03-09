# Ai.py

import openai  # EN: Import OpenAI for AI text generation / SV: Importera OpenAI för AI-textgenerering
from gtts import gTTS  # EN: Import Google Text-to-Speech for converting text to speech / SV: Importera Google Text-to-Speech för att konvertera text till tal
import os  # EN: Import OS module to handle file paths / SV: Importera OS-modulen för att hantera filsökvägar
from Dir import dir  # EN: Import Dir for managing paths and API keys / SV: Importera Dir för att hantera sökvägar och API-nycklar


class AI:
    """EN: Class for AI-driven question and response generation, as well as text-to-speech functionality.
       SV: Klass för AI-genererad fråge- och svarsgenerering samt text-till-tal-funktionalitet."""

    def __init__(self):
        self.text = ""  # EN: Stores the text used for generating questions / SV: Lagrar texten som används för att generera frågor
        self.latest_question = ""  # EN: Stores the latest generated question / SV: Lagrar den senast genererade frågan
        self.audio_path = None  # EN: Stores the path to the generated speech file / SV: Lagrar sökvägen till den genererade ljudfilen
        self.chat_history = []  # EN: Stores chat history for memory / SV: Lagrar chattens historik för minne

        # EN: Set API key and model from Dir.py / SV: Ställ in API-nyckel och modell från Dir.py
        self.api_key = dir.OPENAI_API_KEY
        self.model = dir.GPT_MODEL
        openai.api_key = self.api_key  # EN: Set OpenAI API key / SV: Ställ in OpenAI API-nyckel

    def generate_response(self, user_message):
        """EN: Generates an AI response while ensuring safety by avoiding harmful content.
           SV: Genererar ett AI-svar samtidigt som det säkerställs att inget skadligt innehåll inkluderas."""
        if not user_message:
            return "I am here to listen. How can I help you?"

        # EN: Store the user's message in chat history / SV: Lagra användarens meddelande i chattens historik
        self.chat_history.append({"role": "user", "content": user_message})
        if len(self.chat_history) > 10:
            self.chat_history.pop(0)  # EN: Keep memory limited to last 10 messages / SV: Begränsa minnet till de senaste 10 meddelandena

        prompt = (
            "You are a friendly and empathetic AI that helps people with emotional concerns."
            " Always respond in a supportive, non-harmful, and positive manner."
            " Avoid giving medical advice or discussing self-harm."
            " Encourage the user to seek professional help when necessary."
            " If the user shows signs of mental health issues, gently guide them to seek professional help and to contact 1177 in Sweden."
            " Your response must always consist of exactly two complete sentences."
        )

        messages = [{"role": "system", "content": prompt}] + self.chat_history
        print("📝 Generating AI response with memory...")

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=70,  # EN: Limit response length to a single sentence / SV: Begränsa svarslängden till en mening
                temperature=0.3,
            )
            ai_response = response['choices'][0]['message']['content'].strip()
            print(f"✅ AI response generated: {ai_response}")

            # EN: Store AI response in chat history / SV: Lagra AI-svar i chattens historik
            self.chat_history.append({"role": "assistant", "content": ai_response})
            return ai_response
        except Exception as e:
            print(f"❌ Error generating AI response: {e}")
            return "I am having trouble generating a response at the moment. Please try again later."

    def set_text(self, text):
        """EN: Sets the text used for generating questions.
           SV: Sätter texten som används för att generera frågor."""
        self.text = text
        print("✅ Text set in AI for question generation.")

    def generate_question(self):
        """EN: Generates a question based on the stored text using OpenAI's API.
           SV: Genererar en fråga baserat på den lagrade texten med hjälp av OpenAI:s API."""
        if not self.text:
            print("❌ No text loaded for generating a question.")
            return None, None

        prompt = (
            f"Generate an interesting and relevant question based on the following text:\n\n{self.text}\n\n"
            "The question should be clear, relevant, and contextual."
        )
        print("📝 GPT-3.5 prompt created.")

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an intelligent question generator."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7,
            )
            self.latest_question = response['choices'][0]['message']['content'].strip()
            print(f"✅ Question generated: {self.latest_question}")

            self.audio_path = self.text_to_speech(self.latest_question)
            return self.latest_question, self.audio_path
        except Exception as e:
            print(f"❌ Error generating question: {e}")
            return None, None

    def text_to_speech(self, text, language="sv"):
        """EN: Converts given text into speech using Google Text-to-Speech and saves it as an audio file.
           SV: Konverterar given text till tal med Google Text-to-Speech och sparar det som en ljudfil."""
        if not text:
            print("❌ No text for text-to-speech conversion.")
            return None

        try:
            tts = gTTS(text=text, lang=language, slow=False)
            audio_dir = dir.AUDIO_DIR
            if not os.path.exists(audio_dir):
                os.makedirs(audio_dir)

            audio_path = os.path.join(audio_dir, "question.mp3")
            tts.save(audio_path)
            print(f"🔊 Audio file created: {audio_path}")
            return audio_path
        except Exception as e:
            print(f"❌ Error in text-to-speech conversion: {e}")
            return None
