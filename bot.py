import os
import logging
from config import Config
from pyrogram import Client

if not os.path.isdir(Config.download_dir):
    os.makedirs(Config.download_dir)
plugins = dict(root="plugins")
bot = Client(name="RVX_bot", bot_token=Config.BOT_TOKEN, api_id=Config.API_ID, api_hash=Config.API_HASH, plugins=plugins)

if __name__ == "__main__" :
    bot.run()
