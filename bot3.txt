from pyrogram import Client, filters, types
import asyncio, os, time, math, psutil
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from threading import Thread
from config import Config
from plugins.dl_up_1 import upload_from_url
from Func.headers import get_headers, add_header, reset_headers
from Func.cookie import w_cookies
import globals


API_ID = Config.API_ID
API_HASH = Config.API_HASH
BOT_TOKEN = Config.BOT_TOKEN
M_CHAT = int(Config.M_CHAT)
AUTH_U = Config.AuthU

if not all([API_ID, API_HASH, BOT_TOKEN,M_CHAT,AUTH_U]):
    raise ValueError("API_ID, API_HASH, M_CHAT and BOT_TOKEN environment variables must be set.")

flask_app = Flask(__name__)
CORS(flask_app)

@flask_app.route('/')
def site1_home():
    return "Welcome to Site 1 this can help for uper"


if not os.path.isdir(Config.download_dir):
    os.makedirs(Config.download_dir)
plugins = dict(root="plugins")
app = Client(name="RVX_bot", bot_token=Config.BOT_TOKEN, api_id=Config.API_ID, api_hash=Config.API_HASH, plugins=plugins)

# Start the Pyrogram Client in the main thread
app.start()

def run_upload_t(app, chat_id, video_url, n_caption):
    # Instead of using asyncio.run, use asyncio.run_coroutine_threadsafe to run the coroutine in the main loop
    asyncio.run_coroutine_threadsafe(upload_from_url(app, chat_id=int(chat_id), url=video_url, n_caption=n_caption), app.loop)

def process_tasks():
    """Monitors the tasks dictionary and processes tasks when available."""
    while True:
        if globals.tasks and globals.run == 0:  # Check if the tasks dictionary is not empty
            for chat_id, urls in list(globals.tasks.items()):
                if globals.tasks[chat_id]:  # Ensure the task list for chat_id is not empty
                    globals.run = 1
                    url = globals.tasks[chat_id].pop()  # Pop a URL from the task list
                    for key in globals.task_help:
                        if key in url:
                            setting = globals.task_help[key]
                            if "headers" in setting:
                                for kk in setting["headers"]:
                                    v = setting["headers"]
                                    for hk in v:
                                        hv = v[hk]
                                        add_header(hk, hv)
                            if "cookie" in setting:
                                w_cookies(setting["cookie"])
                    upload_thread = Thread(target=run_upload_t, args=(app, chat_id, url, None))
                    upload_thread.start()
                else:
                    globals.run = 0
                    del globals.tasks[chat_id]  # Remove the task for the chat_id after processing
                    print(f"Completed tasks for chat_id {chat_id}")
                    asyncio.run_coroutine_threadsafe(app.send_message(chat_id=chat_id, text="🔰**Completed** Your tasks...✅️"), app.loop)


@flask_app.route('/makefree')
async def pr_free():
    if globals.progress_s != "free" and "error" in globals.progress_s and globals.run == 0:
        globals.progress_s = "free"
        return jsonify({"s":1,"message":"success!"})
    else:
        return jsonify({"s":0,"message": "Not Errored!"})
        

@flask_app.route('/progress')
def s_pro():
    return jsonify({"s":1,"progress": globals.progress_s,"message":"success!"})


@flask_app.route('/upload', methods=['GET'])
def upload_video():
    chat_id = int(request.args.get('chatid'))
    video_url = request.args.get('url')
    n_caption = request.args.get('cap')
    if not chat_id or not video_url:
        return jsonify({"s":0,"message": "No parameter found!"})
    if not n_caption:
        n_caption = None
    if globals.run != 0:
        return jsonify({"s":0,"message": "Sorry bot is busy right now try again later!"})
    try:
        upload_thread = Thread(target=run_upload_t, args=(app, chat_id, video_url, n_caption))
        upload_thread.start()
        globals.run = 1
        return jsonify({"s":1,"message": "Video added to Uploading!","resd":f"chat_id: {chat_id} & url: {video_url}"})
    except Exception as e:
        return jsonify({"s":0,"message": f"Err on run: {e}","resd":f"chat_id: {chat_id} & url: {video_url}"})


def run_flask():
    flask_app.run(host='0.0.0.0', port=5001)

flask_thread = Thread(target=run_flask)
flask_thread.start()

if __name__ == "__main__":
    #app.run()
    pass
