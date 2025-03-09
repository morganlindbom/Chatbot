# login_window.py

import tkinter as tk
from tkinter import messagebox


class LoginWindow:
    """Creates a login window using Tkinter."""

    def __init__(self, root):
        """Initialize the login window."""
        self.root = root
        self.root.title("Logg in")
        self.root.geometry("300x250")
        self.root.resizable(False, False)

        # Create a frame for the login box
        self.frame = tk.Frame(root, padx=10, pady=10)
        self.frame.pack(pady=10, fill="both", expand=True)

        # Title label
        self.title_label = tk.Label(self.frame, text="Logg in", font=("Arial", 14, "bold"))
        self.title_label.pack(pady=(0, 5))

        # Email label and entry field
        self.email_label = tk.Label(self.frame, text="email:", font=("Arial", 10))
        self.email_label.pack(anchor="w")
        self.email_entry = tk.Entry(self.frame, font=("Arial", 12), width=25)
        self.email_entry.pack(pady=2)

        # Password label and entry field
        self.password_label = tk.Label(self.frame, text="Password:", font=("Arial", 10))
        self.password_label.pack(anchor="w")
        self.password_entry = tk.Entry(self.frame, font=("Arial", 12), width=25, show="*")
        self.password_entry.pack(pady=2)

        # Button frame
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(pady=10)

        # Cancel button
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", font=("Arial", 10), width=10, command=self.on_cancel)
        self.cancel_button.pack(side="left", padx=5)

        # Login button
        self.login_button = tk.Button(self.button_frame, text="Logg in", font=("Arial", 10), width=10, command=self.on_login)
        self.login_button.pack(side="left", padx=5)

    def on_login(self):
        """Handles the login button click event."""
        email = self.email_entry.get()
        password = self.password_entry.get()
        messagebox.showinfo("Login Attempt", f"Email: {email}\nPassword: {password}")

    def on_cancel(self):
        """Closes the login window when Cancel is clicked."""
        self.root.destroy()


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
