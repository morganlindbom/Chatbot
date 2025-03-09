# firebase_service.py

import firebase_admin
from firebase_admin import credentials, auth, firestore
import logging
import datetime
import os
from Dir import dir
from tkinter import messagebox


class FirebaseService:
    """Handles Firebase Authentication and Firestore database operations"""

    def __init__(self):
        # Initialize Firebase if it hasn't been initialized yet
        if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
            cred_path = os.path.join(dir.BASE_DIR, "chatbot-mental-health-firebase-adminsdk-fbsvc-9359ee4d08.json")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()
        logging.basicConfig(level=logging.INFO)

    def authenticate_user(self, email, password, status_label, auth_button):
        try:
            user = auth.get_user_by_email(email)
            logging.info(f"User found: {user.email}, UID: {user.uid}")
            status_label.config(text="Inloggning lyckades", fg="green")
            auth_button.config(text="Logga ut")
            return {"success": True, "message": "User found", "uid": user.uid}

        except auth.UserNotFoundError:
            logging.warning(f"User {email} not found in Firebase Authentication.")
            response = messagebox.askyesno("Registrera konto", "Användaren finns inte. Vill du skapa ett konto?")
            if response:
                register_response = self.register_user(email, password)
                if register_response["success"]:
                    status_label.config(text="Konto skapat! Tryck på Logga in.", fg="green")
                    return register_response
            return {"success": False, "message": "Användaren hittades inte"}

        except Exception as e:
            logging.error(f"Authentication error: {e}")
            return {"success": False, "message": "Serverfel"}

    def register_user(self, email, password):
        try:
            user = auth.create_user(email=email, password=password)
            logging.info(f"User created in Firebase Authentication: {user.uid}")
            doc_id = email.replace("@", "_at_").replace(".", "_dot_")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            today = datetime.datetime.now().strftime("%Y-%m-%d")

            # ✅ Create user document in Firestore with today as an empty list
            user_doc_ref = self.db.collection("Users").document(doc_id)
            user_doc_ref.set({
                "account_info": {
                    "email": email,
                    "password": password,
                    "uid": user.uid,
                    "created_at": timestamp
                },
                "chat_history": {today: []}  # ✅ Initialize today as a list
            }, merge=True)

            logging.info(f"Firestore document created for {email}")
            return {"success": True, "message": "User registered successfully"}
        except Exception as e:
            logging.error(f"Signup error: {e}")
            return {"success": False, "message": str(e)}

    def check_user_exists(self, email):
        """Checks if a user exists in Firebase Authentication."""
        try:
            auth.get_user_by_email(email)
            return True  # ✅ User exists
        except auth.UserNotFoundError:
            return False  # ❌ User does not exist
        except Exception as e:
            logging.error(f"❌ Error checking user existence: {e}")
            return False

    def log_chat(self, email, user_message, ai_message):
        """Logs chat messages under today's date, where today's entry is a list and each message is a dictionary."""
        try:
            doc_id = email.replace("@", "_at_").replace(".", "_dot_")
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            today = datetime.datetime.now().strftime("%Y-%m-%d")

            user_ref = self.db.collection("Users").document(doc_id)
            user_doc = user_ref.get()

            if user_doc.exists:
                user_data = user_doc.to_dict()
                chat_history = user_data.get("chat_history", {})

                # ✅ Ensure today's entry is a list
                if today not in chat_history or not isinstance(chat_history[today], list):
                    chat_history[today] = []  # Store messages directly as a list

                # ✅ Store each message as a dictionary inside the `today` list
                chat_entry = {
                    "1. timestamp": timestamp,
                    "2. user": user_message,
                    "3. ai": ai_message
                }

                chat_history[today].append(chat_entry)  # Append message dictionary inside today's list

                print(f"📝 Saving chat history: {chat_history}")

                # ✅ Save the updated chat history
                user_ref.set({"chat_history": chat_history}, merge=True)

                logging.info(f"✅ Chat log saved for {email} under {today}")
                return {"success": True, "message": "Chat logged"}
            else:
                logging.warning(f"❌ User {email} not found in Firestore.")
                return {"success": False, "message": "User not found"}

        except Exception as e:
            logging.error(f"❌ Error saving chat: {e}")
            return {"success": False, "message": "Error saving chat"}

    def get_user_messages_by_date(self, email, date):
        """Hämtar alla 'user' meddelanden från chatten för ett specifikt datum."""
        try:
            if not email:
                logging.error("❌ Ingen e-postadress angiven för att hämta meddelanden.")
                return []

            doc_id = email.replace("@", "_at_").replace(".", "_dot_")
            user_ref = self.db.collection("Users").document(doc_id)
            user_doc = user_ref.get()

            if user_doc.exists:
                user_data = user_doc.to_dict()
                chat_history = user_data.get("chat_history", {})

                # ✅ Kontrollera om datumet finns
                if date not in chat_history:
                    logging.info(f"Inga chattar hittades för {date}.")
                    return []

                # ✅ Hämta alla 'user'-meddelanden från listan
                user_messages = [entry["2. user"] for entry in chat_history[date] if "2. user" in entry]

                logging.info(f"📌 Hittade {len(user_messages)} meddelanden för {date}: {user_messages}")
                return user_messages

            else:
                logging.warning(f"❌ Användaren {email} hittades inte i Firestore.")
                return []

        except Exception as e:
            logging.error(f"❌ Fel vid hämtning av chattmeddelanden: {e}")
            return []

    def show_user_messages(self, email, date):
        """Hämtar och visar alla 'user' meddelanden från ett specifikt datum i en popup."""
        user_messages = self.get_user_messages_by_date(email, date)

        if user_messages:
            messagebox.showinfo("Användarmeddelanden", "\n".join(user_messages))
        else:
            messagebox.showinfo("Användarmeddelanden", "Inga användarmeddelanden hittades.")

    def logout_user(self, status_label, auth_button):
        """Logs out the user and updates the UI."""
        status_label.config(text="Du har loggat ut", fg="red")
        auth_button.config(text="Logga in")
        logging.info("✅ User logged out successfully.")
        return {"success": True, "message": "User logged out"}
