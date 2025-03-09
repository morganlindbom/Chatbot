# Main.py

import tkinter as tk  # EN: Import Tkinter for GUI / SV: Importera Tkinter för GUI
from chatbot_gui import ChatbotApp  # EN: Import the chatbot GUI class / SV: Importera chatbot GUI-klassen
from Ai import AI  # EN: Import AI class for response generation / SV: Importera AI-klassen för svarsgenerering


class MainApp:
    """EN: Main application that integrates the chatbot GUI and AI response system.
       SV: Huvudapplikationen som integrerar chatbot GUI och AI-svarssystemet."""

    def __init__(self):
        self.root = tk.Tk()  # EN: Create the main Tkinter window / SV: Skapa huvudfönstret i Tkinter
        self.ai = AI()  # EN: Instantiate the AI class / SV: Skapa en instans av AI-klassen
        self.chatbot = ChatbotApp(self.root, self.get_ai_response)  # EN: Initialize the chatbot GUI and connect AI response function / SV: Initiera chatbot GUI och koppla AI-svarsfunktionen

    def get_ai_response(self, user_message):
        """EN: Fetch AI-generated response based on the user's message.
           SV: Hämta AI-genererat svar baserat på användarens meddelande."""
        response = self.ai.generate_response(user_message)  # EN: Call AI class method to generate a response / SV: Anropa AI-klassens metod för att generera ett svar
        self.chatbot.scroll_chat_to_bottom()  # EN: Scroll the chat window to the bottom after response / SV: Skrolla chattfönstret längst ner efter svar
        return response

    def run(self):
        """EN: Start the main application loop.
           SV: Starta huvudapplikationens loop."""
        self.root.mainloop()  # EN: Start the Tkinter event loop / SV: Starta Tkinter-händelseloopen


if __name__ == "__main__":
    app = MainApp()  # EN: Create an instance of MainApp / SV: Skapa en instans av MainApp
    app.run()  # EN: Run the application / SV: Kör applikationen


# pip install openai gtts tkinter
# pip install requests pillow
# pip install firebase-admin
# pip install matplotlib
