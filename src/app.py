import threading

import gradio as gr
import json
import config_paths
import chat_bot
import stream_bot

settings_file_path = config_paths.get_config_file_path()

lore_file_paths = {
    "bot1": config_paths.get_bot1_lore_file_path(),
    "bot2": config_paths.get_bot2_lore_file_path()
}

# Create our initial instance of ChatBotManager
bot_object = chat_bot.ChatBotManager(lore_file_paths)


def save_model_choice(model_choice, settings_file=settings_file_path):
    settings_object = {'model_choice': model_choice}
    with open(settings_file, 'w') as file:
        json.dump(settings_object, file, indent=4)


def load_model_choice(settings_file=settings_file_path):
    with open(settings_file, 'r') as file:
        settings_object = json.load(file)
        return settings_object.get("model_choice", "GPT")  # Provide a default model


def update_chat(user_message, chat_history):
    # Get a bot response for the chat window
    bot_response = bot_object.chat_bot(user_input=user_message)

    # Add the users message to the chat history
    updated_chat_history = chat_history + f"\nYou: {user_message}"

    # have bot respond
    updated_chat_history += f"\nBot: {bot_response}"

    return updated_chat_history, ""


def bot_converse():
    bot_object.initiate_conversation()


with gr.Blocks() as main:
    with gr.Row():
        with gr.Column():
            # Left side components
            last_model_choice = load_model_choice()
            if last_model_choice not in ["GPT", "Oobabooga", "CharacterAI"]:
                last_model_choice = "GPT"
            model_dropdown = gr.Dropdown(label="Select Model",
                                         choices=["GPT", "Oobabooga", "CharacterAI"],
                                         value=last_model_choice)
            model_dropdown.change(save_model_choice, inputs=model_dropdown, outputs=None)

            twitch_username_input = gr.Textbox(label="Twitch Username",
                                               placeholder="Enter your Twitch username here...")
            twitch_token_input = gr.Textbox(label="Twitch Token",
                                            placeholder="Enter your Twitch token here...")
            start_twitch_button = gr.Button("Start/Resume Twitch Connection")
            stop_twitch_button = gr.Button("Pause Twitch Connection")
            twitch_status_output = gr.Textbox(label="Twitch Connection Status", interactive=False)


            def handle_start_twitch_connection(username, token):
                if stream_bot.is_bot_running():
                    # If bot is already created, check if it's paused and resume
                    return stream_bot.resume_bot_if_paused()
                else:
                    # If bot is not created, start it
                    return stream_bot.start_twitch_connection(username, token)


            start_twitch_button.click(
                fn=handle_start_twitch_connection,
                inputs=[twitch_username_input, twitch_token_input],
                outputs=twitch_status_output
            )

            stop_twitch_button.click(
                fn=stream_bot.pause_twitch_bot,
                inputs=[],
                outputs=twitch_status_output
            )
        with gr.Row():
            bots_converse_button = gr.Button("Start Bot Conversation")

        with gr.Column():
            # Right side components
            updated_image = gr.Image()
            current_requester = gr.Textbox(label="Current Requester", interactive=False)
            twitch_feed = gr.Textbox(label="Twitch Feed", interactive=False)
            answer1 = gr.Textbox(label="Answer 1", interactive=False)
            answer2 = gr.Textbox(label="Answer 2", interactive=False)
            answer3 = gr.Textbox(label="Answer 3", interactive=False)

            bots_converse_button.click(
                fn=bot_converse
            )

with gr.Blocks() as chat_interface:
    with gr.Row():
        chat_display = gr.Textbox(label="Chat Display", interactive=False, lines=20)

    with gr.Row():
        chat_window_input = gr.Textbox(label="Your Message",
                                       placeholder="Type your message here...",
                                       interactive=True)
        chat_send_button = gr.Button("Send")

        # Link send button
        chat_send_button.click(
            fn=update_chat,
            inputs=[chat_window_input, chat_display],
            outputs=[chat_display, chat_window_input]
        )


def start_gradio():
    # Create some stupid ass interface
    tabbed_interface = gr.TabbedInterface(
        [main, chat_interface],
        ["Vtuber", "Chat"]
    )
    tabbed_interface.launch()
