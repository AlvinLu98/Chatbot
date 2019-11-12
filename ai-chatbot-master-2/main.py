"""
main.py

Entry point for the ai-chatbot application
"""

import chatbot
import knowledge_acquisition

if __name__ == "__main__":
    app = chatbot.App()
    chatbot.message("Hello, I am a chatbot for train-related queries!")
    knowledge_acquisition.request_last_booking()
    chatbot.message("How can I help you today?")
    app.run()
