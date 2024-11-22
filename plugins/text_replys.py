#replying commands
from pyrogram import Client, filters, types


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
