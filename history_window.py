# history_window.py

import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random


class HistoryWindow:
    """Creates a history window with a graph and control buttons."""

    def __init__(self, root):
        """Initialize the history window."""
        self.root = root
        self.root.title("History_Window")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # Title Frame
        self.title_frame = tk.Frame(root, padx=10, pady=5)
        self.title_frame.pack(fill="x")

        self.title_label = tk.Label(self.title_frame, text="History_Window", font=("Arial", 14, "bold"))
        self.title_label.pack(side="left")

        self.page_label = tk.Label(self.title_frame, text="3 / 3", font=("Arial", 10))
        self.page_label.pack(side="right")

        # History Label
        self.history_label = tk.Label(root, text="History", font=("Arial", 12, "bold"), anchor="w")
        self.history_label.pack(fill="x", padx=10, pady=(5, 2))

        # Graph Label
        self.graph_label = tk.Label(root, text="Graph of your feelings:", font=("Arial", 10))
        self.graph_label.pack(anchor="w", padx=10, pady=(5, 0))

        # Graph Frame
        self.graph_frame = tk.Frame(root, height=200)
        self.graph_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Initialize Matplotlib figure (Empty at start)
        self.fig = Figure(figsize=(5, 2), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.plot([], [])  # Placeholder empty plot

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Button Frame
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        # Cancel Button
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", font=("Arial", 10), width=10, command=self.on_cancel)
        self.cancel_button.pack(side="left", padx=5)

        # Get Graph Button
        self.get_graph_button = tk.Button(self.button_frame, text="Get graph", font=("Arial", 10), width=10, command=self.generate_graph)
        self.get_graph_button.pack(side="left", padx=5)

    def generate_graph(self):
        """Generates a simple random graph to simulate mood tracking."""
        self.ax.clear()
        self.ax.set_title("Mood Tracking")
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        x_values = list(range(1, 6))  # Example time points
        y_values = [random.randint(1, 10) for _ in range(5)]  # Random mood values

        self.ax.plot(x_values, y_values, marker="o", linestyle="-", color="gray", linewidth=2)
        self.canvas.draw()

    def on_cancel(self):
        """Closes the history window when Cancel is clicked."""
        self.root.destroy()


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = HistoryWindow(root)
    root.mainloop()
