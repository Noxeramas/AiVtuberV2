import openai
import request_manager
import requests
import os


class ChatBotManager:
    def __init__(self):
        self.model_choice = 'GPT'
        self.openai_history = []
        self.ooba_history = {'internal': [], 'visible': []}

    def chat_bot(self, user_input):
        if self.model_choice == 'GPT':

            # Initialize chat history if it's the first request or empty
            if not self.openai_history:
                openai_history = []

            # Prepare the request for the GPT model
            openai_data = request_manager.OpenAIData()
            request = openai_data.request

            # Update the messages with the latest user input and existing chat history
            messages = []
            for message in request["messages"]:
                content = message["content"]
                content = content.replace("user_input", user_input)
                content = content.replace("chat_history", openai_history)
                content = content.replace("lore", lore)
                messages.append({"role": message["role"], "content": content})

            # Make the API call
            response = openai.ChatCompletion.create(
                model=request["model"],
                messages=messages
            )
