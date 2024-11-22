import os
import logging
from config import Config
from pyrogram import Client
from flask import Flask, jsonify, request
from flask_cors import CORS
from threading import Thread

flask_app = Flask(__name__)
CORS(flask_app)

@flask_app.route('/')
def site1_home():
    return "Welcome to Site 1 this can help for uper"


if not os.path.isdir(Config.download_dir):
    os.makedirs(Config.download_dir)
plugins = dict(root="plugins")
bot = Client(name="RVX_bot", bot_token=Config.BOT_TOKEN, api_id=Config.API_ID, api_hash=Config.API_HASH, plugins=plugins)

def run_flask():
    flask_app.run(host='0.0.0.0', port=5000)

flask_thread = Thread(target=run_flask)
flask_thread.start()

if __name__ == "__main__" :
    bot.run()
