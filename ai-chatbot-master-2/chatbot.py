"""
chatbot.py

The main ai-chatbot application
"""

import nlp
import reasoning
import knowledge_base
import tkinter as tk
import os

# Name for user messages
USER_NAME = "You"

# Name for chatbot messages
CHATBOT_NAME = "Chatbot"

# Path to log file
LOG_PATH = "log.txt"

class App:
    """ Main chatbot application class. """

    instances = []

    def __init__(self):
        # Log this instance for messaging
        self.instances.append(self)

        # Main GUI window
        self.window = tk.Tk()
        self.window.title("ai-chatbot")

        # Input field for user messages
        self.input_msg = tk.StringVar()
        self.input_box = tk.Entry(self.window, text=self.input_msg)
        self.input_box.pack(side=tk.BOTTOM, fill=tk.X)
        self.input_box.bind("<Return>", self.submit)

        # Read-only text field for chat history
        self.history = tk.Text(self.window)
        self.history.bind("<Key>", lambda event: "break")
        self.history.pack(side=tk.LEFT, fill=tk.BOTH)

        # Style tags for chat names
        self.history.tag_configure("style_chatbot",
            font="Courier 10 bold",
            foreground="green")

        self.history.tag_configure("style_other",
            font="Courier 10 bold",
            foreground="blue")

        # Scroll bar for chat history
        self.scroll = tk.Scrollbar(self.window, command=self.history.yview)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.history["yscrollcommand"] = self.scroll.set

        # Mark new start in chat log
        log = open(LOG_PATH, "a")
        log.write("\n\n--------\n\n\n")
        log.close()

    def run(self):
        """ Runs the application main loop. """
        self.window.mainloop()

    def log_message(self, name, msg):
        """ Sends a message into the chat history.

        Args:
            name: String of sender's name.
            msg: String of message to send.
        """
        self.history.insert(tk.INSERT, name,
            "style_chatbot" if name == "Chatbot" else "style_other")
        self.history.insert(tk.INSERT, f": {msg}\n\n")

        log = open(LOG_PATH, "a")
        log.write(f"{name}: {msg}\n")
        log.close()

    def submit(self, event):
        """ Submits the user message and reasons the chatbot response. """
        msg = self.input_msg.get()
        self.input_msg.set("")
        if msg:
            self.log_message(USER_NAME, msg)
            query_tokens = nlp.process_query(msg)
            intent = reasoning.reason_standard(query_tokens)
            information_tokens = nlp.process_parameters(msg, intent)
            knowledge_base.respond(intent, information_tokens)
            
            message("How can I help you today?")


def message(msg):
    """ Has the chatbot send a message.

    Args:
        msg: String message to send.
    """
    for app in App.instances:
        app.log_message(CHATBOT_NAME, msg)
