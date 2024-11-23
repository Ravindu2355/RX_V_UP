import os,time
from pyrogram import Client as app
from pyrogram import filters, types
from config import Config
from Func.reply_text import Text
import psutil
from Func.headers import get_headers, add_header, reset_headers
from plugins.dl_up_1 import upload_from_url
import globals

def run_upload_t(app, chat_id, video_url, n_caption):
    asyncio.run(upload_from_url(app, chat_id=int(chat_id), url=video_url, n_caption=n_caption))

def process_tasks():
    """Monitors the tasks dictionary and processes tasks when available."""
    while True:
        if globals.tasks and globals.run == 0:  # Check if the tasks dictionary is not empty
            for chat_id, urls in list(globals.tasks.items()):
                if globals.tasks[chat_id]:  # Ensure the task list for chat_id is not empty
                    globals.run = 1
                    url = globals.tasks[chat_id].pop()  # Pop a URL from the task list
                    upload_thread = Thread(target=run_upload_t, args=(app, chat_id, url, None))
                    upload_thread.start()
                else:
                    globals.run = 0
                    del globals.tasks[chat_id]  # Remove the task for the chat_id after processing
                    print(f"Completed tasks for chat_id {chat_id}")
        else:
            time.sleep(1)

@app.on_message(filters.private & filters.command("start"))
async def _start(client,message:types.Message):
    if str(message.chat.id) in Config.AuthU:
        un=message.chat.username
        st=Text.start
        if un:
            nun=un
        else:
            nun=message.chat.first_name
        if nun:
          st=st.replace("R-user",nun)
        st=st.replace("user_id",str(message.chat.id))
        reply_msg = await message.reply(st)
    else:
        await message.delete();
        
@app.on_message(filters.private & filters.command("help"))
async def _help(client,message:types.Message):
    await app.send_message(Text.help)
    
@app.on_message(filters.private & filters.command("ping"))
async def c_pin(client,message:types.Message):
    start_time = time.time()  # Record start time
    reply_msg = await message.reply("🔰Ping checking...🔰")
    end_time = time.time()  # Record end time after sending
    latency = (end_time - start_time) * 1000  # Convert to milliseconds
    await reply_msg.edit_text(f"Ping: {latency:.2f} ms")

@app.on_message(filters.private & filters.command("disc"))
async def c_disc(client,message:types.Message):
    disk_usage = psutil.disk_usage('/')
    total_space = disk_usage.total / (1024 ** 3)  # Convert to GB
    used_space = disk_usage.used / (1024 ** 3)    # Convert to GB
    free_space = disk_usage.free / (1024 ** 3)    # Convert to GB
    await message.reply(
        f"Disk Space:\n"
        f"Total: {total_space:.2f} GB\n"
        f"Used: {used_space:.2f} GB\n"
        f"Free: {free_space:.2f} GB"
      )

#header control......
@app.on_message(filters.private & filters.command("add_h"))
async def _add_h(client,message:types.Message):
    if str(message.chat.id) in Config.AuthU:
        hs=message.text.split(" ")
        if hs[1] and "--" in hs[1]:
            ks=hs[1].split("--")
            k=ks[0]
            v=ks[1]
            add_header(k,v)
            await message.reply(f"header setteded!\nkey:{k} value:{v}")
        else:
            await message.reply("No header string! use /add_h key--value")
    else:
        await message.reply("You are not my auther!🫠")


@app.on_message(filters.private & filters.command("del_h"))
async def _del_h(client,message:types.Message):
    if str(message.chat.id) in Config.AuthU:
        reset_headers()
        await message.reply("headers reseted!")
    else:
        await message.reply("You are not my auther!🫠")


@app.on_message(filters.private & filters.command("get_h"))
async def _get_h(client,message:types.Message):
    if str(message.chat.id) in Config.AuthU:
        hh=get_headers()
        await message.reply(f"This is my defalt headers:\n{json.dumps(hh)}")
    else:
        await message.reply("You are not my auther!🫠")
    
@app.on_message(filters.private & filters.command("tasks"))
async def _p_tasks(client,message:types.Message):
    if str() in Config.AuthU:
        listn_tasks=Thread(target=process_tasks, daemon=True)
        listn_tasks.start()
        await message.reply("Listn Started!...")
    else:
        await message.reply("You are not my auther!🫠")
