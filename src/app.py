import gradio as gr
import json
import config_paths

settings_file_path = config_paths.get_settings_file_path()


def handle_interaction(model_choice):
    save_model_choice(model_choice)


def save_model_choice(model_choice, settings_file=settings_file_path):
    settings_object = {'model_choice': model_choice}
    with open(settings_file, 'w') as file:
        json.dump(settings_object, file, indent=4)


def load_model_choice(settings_file=settings_file_path):
    with open(settings_file, 'r') as file:
        settings_object = json.load(file)
        return settings_object.get("model_choice", "GPT")  # Provide a default model


with gr.Blocks() as main:
    with gr.Row():
        last_model_choice = load_model_choice()
        if last_model_choice not in ["GPT", "Oobabooga", "CharacterAI"]:
            last_model_choice = "GPT"
        model_dropdown = gr.Dropdown(label="Select Model",
                                     choices=["GPT", "Oobabooga", "CharacterAI"],
                                     value=last_model_choice)
        model_dropdown.change(save_model_choice, inputs=model_dropdown, outputs=None)

        chat_window = gr.Textbox(label="Chat Window", interactive=False)
        chat_window_input = gr.Textbox(label="Your Message", placeholder="Type your message here...")

with gr.Blocks() as settings:
    with gr.Row():
        settings_text = gr.Textbox(label="Settings", interactive=False)
        settings_text_input = gr.Textbox(label="Settings", interactive=False)
        settings_text_input.text = "Settings will be here soon!"


def start_gradio():
    # Create some stupid ass interface
    tabbed_interface = gr.TabbedInterface(
        [main, settings],
        ["Chat Window", "Settings"]
    )
    tabbed_interface.launch()
