import asyncio
import os
import time
from threading import Thread
from flask import Flask, jsonify, request
from flask_cors import CORS
from pyrogram import Client
from config import Config
from plugins.dl_up_1 import upload_from_url
import globals

# Initialize API_ID, API_HASH, and BOT_TOKEN from Config
API_ID = Config.API_ID
API_HASH = Config.API_HASH
BOT_TOKEN = Config.BOT_TOKEN
M_CHAT = int(Config.M_CHAT)
AUTH_U = Config.AuthU

if not all([API_ID, API_HASH, BOT_TOKEN, M_CHAT, AUTH_U]):
    raise ValueError("API_ID, API_HASH, M_CHAT and BOT_TOKEN environment variables must be set.")

# Create Flask app and enable CORS
flask_app = Flask(__name__)
CORS(flask_app)

# Setup the Pyrogram client
app = Client(name="RVX_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Create Flask routes
@flask_app.route('/')
def site1_home():
    return "Welcome to Site 1 this can help for upload."

@flask_app.route('/makefree')
async def pr_free():
    if globals.progress_s != "free" and "error" in globals.progress_s and globals.run == 0:
        globals.progress_s = "free"
        return jsonify({"s": 1, "message": "success!"})
    else:
        return jsonify({"s": 0, "message": "Not Errored!"})

@flask_app.route('/progress')
def s_pro():
    return jsonify({"s": 1, "progress": globals.progress_s, "message": "success!"})

def run_upload_t(chat_id, video_url, n_caption):
    asyncio.run(upload_from_url(app, chat_id=int(chat_id), url=video_url, n_caption=n_caption))

@flask_app.route('/upload', methods=['GET'])
def upload_video():
    chat_id = int(request.args.get('chatid'))
    video_url = request.args.get('url')
    n_caption = request.args.get('cap')
    if not chat_id or not video_url:
        return jsonify({"s": 0, "message": "No parameter found!"})
    if not n_caption:
        n_caption = None
    if globals.run != 0:
        return jsonify({"s": 0, "message": "Sorry, the bot is busy right now. Try again later!"})
    try:
        # Start the upload task in a new thread
        upload_thread = Thread(target=run_upload_t, args=(chat_id, video_url, n_caption))
        upload_thread.start()
        globals.run = 1
        return jsonify({"s": 1, "message": "Video added to Uploading!", "resd": f"chat_id: {chat_id} & url: {video_url}"})
    except Exception as e:
        return jsonify({"s": 0, "message": f"Error during upload: {e}", "resd": f"chat_id: {chat_id} & url: {video_url}"})


def process_tasks():
    while True:
        if globals.tasks and globals.run == 0:
            for chat_id, urls in list(globals.tasks.items()):
                if globals.tasks[chat_id]:
                    globals.run = 1
                    url = globals.tasks[chat_id].pop()
                    upload_thread = Thread(target=run_upload_t, args=(chat_id, url, None))
                    upload_thread.start()
                else:
                    globals.run = 0
                    del globals.tasks[chat_id]
                    print(f"Completed tasks for chat_id {chat_id}")
        else:
            time.sleep(1)

def run_flask():
    flask_app.run(host='0.0.0.0', port=5000)

def start_client():
    with app:
        # Start the Flask app in a separate thread
        flask_thread = Thread(target=run_flask)
        flask_thread.start()

        # Start the task processing
        listn_tasks = Thread(target=process_tasks, daemon=True)
        listn_tasks.start()


if __name__ == "__main__":
    # Start the Pyrogram client and Flask app
    start_client()
