import gradio as gr
import json
import config_paths
import stream_bot
from bot_manager import bot_object
from config_manager import ConfigManager

settings_file_path = config_paths.get_config_file_path()

config_manager = ConfigManager(settings_file_path)

lore_file_paths = {
    "bot1": config_paths.get_bot1_lore_file_path(),
    "bot2": config_paths.get_bot2_lore_file_path()
}

# Define state objects
twitch_username_state = gr.State()
twitch_token_state = gr.State()
openai_api_key_state = gr.State()


def save_model_choice(model_choice, settings_file=settings_file_path):
    settings_object = {'model_choice': model_choice}
    with open(settings_file, 'w') as file:
        json.dump(settings_object, file, indent=4)


def load_model_choice(settings_file=settings_file_path):
    with open(settings_file, 'r') as file:
        settings_object = json.load(file)
        return settings_object.get("model_choice", "GPT")  # Provide a default model


def save_all_settings(twitch_username, twitch_token, api_key):
    config_manager.set_setting(['streaming_platforms', 'twitch', 'username'], twitch_username)
    config_manager.set_setting(['streaming_platforms', 'twitch', 'token'], twitch_token)
    config_manager.set_setting(['streaming_platforms', 'openai', 'api_key'], api_key)
    config_manager.save_settings()
    return "Settings saved successfully!"


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


def handle_start_twitch_connection(username, token):
    twitch_bot_instance = stream_bot.twitch_bot_instance
    if twitch_bot_instance:
        # Check if the bot is paused
        if not twitch_bot_instance.active:
            # If bot is paused, resume it
            return stream_bot.resume_twitch_bot()
        else:
            # If bot is active, indicate that the connection is already active
            return "Twitch connection is already active."
    else:
        # If bot is not running, start a new connection and save the settings
        response = stream_bot.start_twitch_connection(username, token)
        config_manager.set_setting("twitch_username", username)
        config_manager.set_setting("twitch_token", token)
        return response


def handle_gradio_inputs():
    # Load our settings into our object

    twitch_username_state.value = config_manager.twitch_username
    twitch_token_state.value = config_manager.twitch_token
    openai_api_key_state.value = config_manager.openai_api_key


def start_gradio():
    handle_gradio_inputs()

    with gr.Blocks(theme='step-3-profit/Midnight-Deep') as main:
        with gr.Tab("AI Vtuber"):
            with gr.Row():
                with gr.Column(scale=1):
                    # AI Model Selection Dropdown
                    last_model_choice = load_model_choice()
                    model_dropdown = gr.Dropdown(label="Select AI Model",
                                                 choices=["GPT", "Oobabooga", "CharacterAI"],
                                                 value=last_model_choice)
                    model_dropdown.change(save_model_choice, inputs=model_dropdown, outputs=None)

                    # Add Twitch connection buttons
                    start_twitch_button = gr.Button("Start/Resume Twitch Connection")
                    stop_twitch_button = gr.Button("Pause Twitch Connection")
                    twitch_status_output = gr.Textbox(label="Twitch Connection Status", interactive=False)

                    start_twitch_button.click(
                        fn=handle_start_twitch_connection,
                        inputs=[twitch_username_state, twitch_token_state],
                        outputs=twitch_status_output
                    )

                    stop_twitch_button.click(
                        fn=stream_bot.pause_twitch_bot,
                        inputs=[],
                        outputs=twitch_status_output
                    )

                    start_conversation_button = gr.Button("Start Conversation")

                with gr.Column(scale=1):
                    # Display for the most recent bot response and an image output
                    current_response = gr.Textbox(label="Current Bot Response", interactive=False)
                    start_conversation_button.click(
                        fn=bot_converse,
                        inputs=[],
                        outputs=[current_response]
                    )

        with gr.Tab("Settings"):
            with gr.Row():
                save_all_settings_button = gr.Button("Save All Settings")
            # Twitch settings

            with gr.Row():
                with gr.Column():
                    with gr.Group():
                        twitch_username_input = gr.Textbox(label="Twitch Username", value=twitch_username_state.value,
                                                           placeholder="Enter Twitch username")
                        twitch_token_input = gr.Textbox(label="Twitch Token", value=twitch_token_state.value,
                                                        placeholder="Enter Twitch token")
                    with gr.Group():
                        youtube_username_input = gr.Textbox(label="YouTube Username", placeholder="Enter YouTube username")
                        youtube_token_input = gr.Textbox(label="YouTube Token", placeholder="Enter YouTube token")

                with gr.Column():
                    openai_api_key_input = gr.Textbox(label="OpenAI API Key", value=openai_api_key_state.value,
                                                  placeholder="Enter OpenAI API key")

            save_all_settings_button.click(
                fn=save_all_settings,
                inputs=[twitch_username_input,
                        twitch_token_input,
                        openai_api_key_input],
                outputs=None
            )

        with gr.Tab("Statistics"):
            with gr.Column():
                # Placeholder components for future statistics or analytics
                stats_display = gr.Textbox(label="Statistics", interactive=False)
                # More components can be added as statistics are implemented

    main.launch()
