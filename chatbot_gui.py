# chatbot_gui.py

import tkinter as tk
from tkinter import scrolledtext, messagebox
from firebase_service import FirebaseService


class ChatbotApp:
    def __init__(self, root, ai_response_function):
        self.root = root
        self.root.title("Mental Health Chatbot")
        self.root.geometry("400x600")
        self.root.configure(bg="#E8F6F3")
        self.ai_response_function = ai_response_function
        self.firebase = FirebaseService()
        self.is_logged_in = False
        self.current_user = None
        self.account_created = False  # Track account creation
        self.create_widgets()

    def create_widgets(self):
        """Create GUI components."""
        self.email_label = tk.Label(self.root, text="Email:", font=("Arial", 12), bg="#E8F6F3")
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(self.root, font=("Arial", 14), bg="white")
        self.email_entry.pack(pady=5, padx=10, fill=tk.X)
        self.email_entry.insert(0, "mogge@kalle.com")  # ✅ Pre-fill email for testing

        self.password_label = tk.Label(self.root, text="Password:", font=("Arial", 12), bg="#E8F6F3")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, font=("Arial", 14), bg="white", show="*")
        self.password_entry.pack(pady=5, padx=10, fill=tk.X)
        self.password_entry.insert(0, "123456")  # ✅ Pre-fill password for testing

        self.auth_button = tk.Button(self.root, text="Logga in", command=self.toggle_auth, font=("Arial", 12), bg="#5DADE2", fg="white")
        self.auth_button.pack(pady=5)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#E8F6F3", fg="red")
        self.status_label.pack(pady=5)

        self.chat_window = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 12), bg="white", fg="black", height=15)
        self.chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.user_input = tk.Entry(self.root, font=("Arial", 14), bg="white")
        self.user_input.pack(padx=10, pady=5, fill=tk.X)

        # Bind Enter key to send message
        self.root.bind("<Return>", lambda event: self.send_message())
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message, font=("Arial", 12), bg="#48C9B0", fg="white")
        self.send_button.pack(pady=5)

        self.show_messages_button = tk.Button(self.root, text="Visa meddelanden", command=self.show_messages)
        self.show_messages_button.pack(pady=5)

    def scroll_chat_to_bottom(self):
        """Scrolls the chat window to the bottom when a new message is added."""
        self.chat_window.yview(tk.END)

    def toggle_auth(self):
        """Handles login and account creation logic."""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            self.status_label.config(text="Vänligen fyll i alla fält", fg="red")
            return

        if self.is_logged_in:
            self.firebase.logout_user(self.status_label, self.auth_button)
            self.is_logged_in = False
            self.current_user = None
            self.auth_button.config(text="Logga in")
            return

        if self.account_created:
            self.status_label.config(text="Konto skapat! Loggar in...", fg="blue")
            self.account_created = False
            self.authenticate(email, password)
            return

        if not self.firebase.check_user_exists(email):
            create_new = messagebox.askyesno("Konto saknas", "Det finns inget konto med denna e-post. Vill du skapa ett nytt?")
            if create_new:
                self.create_account(email, password)
            else:
                self.status_label.config(text="Konto hittades inte", fg="red")
            return

        self.authenticate(email, password)

    def authenticate(self, email, password):
        """Attempts to log in the user."""
        response = self.firebase.authenticate_user(email, password, self.status_label, self.auth_button)
        if response["success"]:
            self.is_logged_in = True
            self.current_user = email
            self.auth_button.config(text="Logga ut")
            self.status_label.config(text="Inloggning lyckades", fg="green")
        else:
            self.status_label.config(text="Felaktig e-post eller lösenord", fg="red")

    def create_account(self, email, password):
        """Creates a new user account."""
        if not email or not password:
            self.status_label.config(text="Fyll i alla fält", fg="red")
            return

        response = self.firebase.register_user(email, password)

        if response.get("success"):
            self.status_label.config(text="Konto skapat! Tryck på Logga in igen.", fg="green")
            self.account_created = True  # Allow login on next click
        else:
            error_message = response.get("error", "Okänt fel")
            if "EMAIL_EXISTS" in error_message:
                self.status_label.config(text="E-postadressen är redan registrerad.", fg="orange")
            else:
                self.status_label.config(text=f"Fel: {error_message}", fg="red")

    def send_message(self):
        """Handles sending user messages, displaying AI responses, and logging both in Firestore."""
        if not self.is_logged_in:
            self.status_label.config(text="Logga in först!", fg="red")
            return

        user_message = self.user_input.get().strip()
        if not user_message:
            return

        self.chat_window.config(state=tk.NORMAL)
        self.chat_window.insert(tk.END, f"You: {user_message}\n", "user")
        self.chat_window.config(state=tk.DISABLED)
        self.user_input.delete(0, tk.END)

        # ✅ Generate AI response
        ai_response = self.ai_response_function(user_message)

        self.chat_window.config(state=tk.NORMAL)
        self.chat_window.insert(tk.END, f"Bot: {ai_response}\n", "bot")
        self.chat_window.config(state=tk.DISABLED)
        self.scroll_chat_to_bottom()

        # ✅ Log both messages together with timestamp
        self.firebase.log_chat(self.current_user, user_message, ai_response)

    def show_messages(self):
        """Calls Firebase function to display user messages"""
        email = self.current_user  # Get the logged-in user
        date = "2025-03-09"  # The date you want to retrieve messages from

        self.firebase.show_user_messages(email, date)  # Call the function in FirebaseService
