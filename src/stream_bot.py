import asyncio
import threading

from twitchio.ext import commands

# Global variable to keep track of our twitch bot instance
twitch_bot_instance = None
event_loop_thread = None


class TwitchBot(commands.Bot):
    def __init__(self, token, channel):
        super().__init__(token=token, prefix='!', initial_channels=[channel])
        self.active = True  # Flag to control message handling

    async def event_ready(self):
        print(f'Logged in as: {self.nick}')

    async def event_message(self, message):
        if not self.active:  # Only process messages if bot is active
            return
        print(message.content)
        await self.handle_commands(message)

    def pause(self):
        self.active = False  # Set the bot to inactive
        print("Bot is paused, it will no longer respond to messages.")

    def resume(self):
        self.active = True  # Set the bot to active
        print("Bot is resumed, it will now respond to messages.")


def start_twitch_connection(username, token):
    global twitch_bot_instance
    global event_loop_thread

    if twitch_bot_instance is not None:
        return "Twitch connection is already active."

    def run_bot():
        global twitch_bot_instance

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        twitch_bot_instance = TwitchBot(token=token, channel=username)
        loop.run_until_complete(twitch_bot_instance.start())

    event_loop_thread = threading.Thread(target=run_bot)
    event_loop_thread.start()

    return "Twitch connection started."


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


def is_bot_paused():
    global twitch_bot_instance
    return twitch_bot_instance is not None and not twitch_bot_instance.active


def resume_bot_if_paused():
    global twitch_bot_instance
    if is_bot_paused():
        twitch_bot_instance.resume()
        return "Bot resumed."
    return "Bot was not paused."
