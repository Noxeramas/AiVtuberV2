from chat_bot import ChatBotManager
import config_paths

lore_paths = {
    "bot1": config_paths.get_bot1_lore_file_path(),
    "bot2": config_paths.get_bot2_lore_file_path()
}

bot_object = ChatBotManager(lore_paths)
