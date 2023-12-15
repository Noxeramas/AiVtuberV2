import asyncio
import random
import threading
import time
from bot_manager import bot_object

from twitchio.ext import commands

# Global variable to keep track of our twitch bot instance
twitch_bot_instance = None
event_loop_thread = None


class TwitchBot(commands.Bot):
    def __init__(self, token, channel):
        super().__init__(token=token, prefix='!', initial_channels=[channel])
        self.active = True  # Flag to control message handling
        self.channel_joined = False

    async def event_ready(self):
        print(f'Logged in as: {self.nick}')
        self.channel_joined = True  # Set to True when a channel is joined

    async def event_message(self, message):
        if not self.active:  # Only process messages if bot is active
            return
        print(message.content)
        await self.handle_commands(message)

    async def handle_commands(self, message):
        print("Handling commands...")
        bot_names = {
            "bot1": "Yumi",
            "bot2": "Kyoko"
        }
        self.determine_bot_response(message.content, bot_names)

    async def event_join(self, channel, user):
        self.channel_joined = True  # Set to True when a channel is joined
        print(f"Joined channel: {channel.name}")

    def is_connection_successful(self):
        return self.channel_joined

    def pause(self):
        self.active = False  # Set the bot to inactive
        print("Bot is paused, it will no longer respond to messages.")

    def resume(self):
        self.active = True  # Set the bot to active
        print("Bot is resumed, it will now respond to messages.")

    def determine_bot_response(self, message_content, bot_names):
        """
        Determines which bot(s) should respond based on the message content.

        :param message_content: The content of the Twitch message.
        :param bot_names: Dictionary containing bot identifiers and their names.
        """
        print("Determining bot response...")
        bot1_name = bot_names["bot1"]
        bot2_name = bot_names["bot2"]
        combined_name_1 = f"{bot1_name} and {bot2_name}"
        combined_name_2 = f"{bot2_name} and {bot1_name}"

        if combined_name_1.lower() in message_content.lower():
            # Bot1 responds first
            bot1_response = bot_object.chat_bot(message_content, "bot1", interaction_type="user")
            # Contextual prompt for Bot2, including Bot1's response
            bot2_contextual_prompt = (
                f"{bot1_name} has already responded: '{bot1_response}'. "
                f"Now, as {bot2_name}, respond to the original query: '{message_content}' "
                f"considering {bot1_name}'s response."
            )
            bot_object.chat_bot(bot2_contextual_prompt, "bot2", interaction_type="user")

        elif combined_name_2.lower() in message_content.lower():
            # Bot2 responds first
            bot2_response = bot_object.chat_bot(message_content, "bot2", interaction_type="user")
            # Contextual prompt for Bot1, including Bot2's response
            bot1_contextual_prompt = (
                f"{bot2_name} has already responded: '{bot2_response}'. "
                f"Now, as {bot1_name}, respond to the original query: '{message_content}' "
                f"considering {bot2_name}'s response."
            )
            bot_object.chat_bot(bot1_contextual_prompt, "bot1", interaction_type="user")

        else:
            # Handle other cases where only one bot or no bots are mentioned
            bot1_mentioned = bot1_name.lower() in message_content.lower()
            bot2_mentioned = bot2_name.lower() in message_content.lower()

            if bot1_mentioned:
                print("Bot1 responds")
                bot_object.chat_bot(message_content, "bot1", interaction_type="user")
            elif bot2_mentioned:
                print("Bot2 responds")
                bot_object.chat_bot(message_content, "bot2", interaction_type="user")
            else:
                print("Random bot responds")
                chosen_bot = random.choice(["bot1", "bot2"])
                bot_object.chat_bot(message_content, chosen_bot, interaction_type="user")


def start_twitch_connection(username, token):
    global twitch_bot_instance
    global event_loop_thread

    if twitch_bot_instance and twitch_bot_instance.is_connected():
        return "Twitch connection is already active."

    def run_bot():
        global twitch_bot_instance

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            twitch_bot_instance = TwitchBot(token=token, channel=username)
            loop.run_until_complete(twitch_bot_instance.start())
        except Exception as e:
            print(f"Error starting Twitch connection: {e}")
            if twitch_bot_instance:
                twitch_bot_instance.connection_successful = False

    event_loop_thread = threading.Thread(target=run_bot)
    event_loop_thread.start()

    time.sleep(5)

    if twitch_bot_instance and twitch_bot_instance.is_connection_successful():
        return "Twitch connection started."
    else:
        twitch_bot_instance = None
        event_loop_thread = None
        return "Failed to start Twitch connection. Please check your username and token."


def pause_twitch_bot():
    global twitch_bot_instance
    if twitch_bot_instance:
        twitch_bot_instance.pause()
        return "Connection Paused."
    return "Bot not running."


def resume_twitch_bot():
    global twitch_bot_instance
    if twitch_bot_instance:
        twitch_bot_instance.resume()
        return "Connection Resumed."
    return "Bot not running."


def is_bot_running():
    global twitch_bot_instance
    return twitch_bot_instance is not None
