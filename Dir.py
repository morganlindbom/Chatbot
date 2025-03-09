import os


class dir:
    """Hantera alla statiska sökvägar i projektet."""

    OPENAI_API_KEY = r"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"

    # 🔥 Definiera GPT här, varianter finns i GptModels.py
    GPT_MODEL = "gpt-3.5-turbo"

    AI_VOICE = "nova"
    # 🎙 **Tillgängliga röster för OpenAI TTS**
    # ----------------------------------------
    # "alloy"   # 🗣 Naturlig, neutral ton (Standard)
    # "echo"    # 🔊 Tydlig och engagerad
    # "fable"   # 📖 Lugn och berättande
    # "onyx"    # 🎭 Djup och allvarlig
    # "nova"    # ✨ Lättsam och mjuk
    # "shimmer" # 🎶 Lätt och melodisk

    # Ai speed in the voice
    AI_SPEED = 0.8

    # 📜 **Lista som sparar frågor indexerat**
    QUESTIONS = [
        # Exempel på lagrade frågor:
        # [
        #     "1. Vad är syftet med Scrum-metoden?",
        #     "A) Att skapa en hierarkisk struktur",
        #     "B) Att ha en flexibel och självorganiserande process",
        #     "C) Att minska behovet av kommunikation i teamet",
        #     "D) Att ge projektledaren full kontroll",
        #     "Rätt svar: B) Att ha en flexibel och självorganiserande process"
        # ]
    ]

    # Sökvägar för filer och ljud
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # 🔊 Ljudfiler
    AUDIO_DIR = os.path.join(BASE_DIR, "temp_audio")
    AUDIO_FILE = os.path.join(AUDIO_DIR, "output.wav")

    # 📄 PDF-filer
    PDF_DIR = os.path.join(BASE_DIR, "pdf_files")
    PDF_FILE = os.path.join(BASE_DIR, "Agile Engineering Software Products_ An Introduction to Modern Software Engineering (2020, Pearson) - libgen.li.pdf")

    # 🔥 Se till att mapparna finns
    os.makedirs(AUDIO_DIR, exist_ok=True)
    os.makedirs(PDF_DIR, exist_ok=True)

    @staticmethod
    def get_audio_dir():
        """Returnerar ljudmappen."""
        return dir.AUDIO_DIR

    @staticmethod
    def get_audio_file():
        """Returnerar den fasta sökvägen till ljudfilen."""
        return dir.AUDIO_FILE

    @staticmethod
    def get_pdf_dir():
        """Returnerar PDF-mappen."""
        return dir.PDF_DIR

    @staticmethod
    def get_pdf_file():
        """Returnerar den fasta sökvägen till PDF-filen."""
        return dir.PDF_FILE
