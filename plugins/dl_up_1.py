#for direct link upload.....(uploader rvx direct)
from pyrogram import Client
from pyrogram import filters, types
import asyncio, os, time, requests, math, psutil, json
from moviepy.editor import VideoFileClip
from PIL import Image
from Func.display_progress import progress_for_pyrogram, humanbytes, TimeFormatter
from Func.cookie import r_cookies, w_cookies, clear_cookies
from Func.headers import load_headers
from Func.simple_func import delete_file, get_file_name_from_response, intt
from Func.reply_text import Text
import globals
from config import Config

sizelimit = Config.TG_MAX_FILE_SIZE

async def upload_from_url(app:Client, chat_id, url: str, n_name=None, n_caption=None, s_type="video",reply_msg=None):
    if reply_msg is None:
        reply_msg = await app.send_message(chat_id=chat_id,text="Processing!....")
    else:
        await reply_msg.edit_text("**🔰RVX🔰**\n\nProcessing....!🛠")
    if not app:
        await reply_msg.reply(f"Er:No app Arg!")
    if not chat_id:
        await reply_msg.reply(f"Er:No chat_id Arg!")
    if not url:
        await reply_msg.reply(f"Er:No url Arg!")
    globals.progress_s="Processing...!"
    globals.run = 1
    try:
        if len(url) < 2:
            await reply_msg.edit_text("😒Please provide a URL!🥲")
            globals.progress_s="free"
            globals.run = 0
            return
        await reply_msg.edit_text("**🔰RVX🔰**\n\nStarting download...")
        globals.progress_s="Download starting...."
        cookies = r_cookies()
        headers = load_headers()
        if not cookies:
            response = requests.get(url, headers=headers, cookies=cookies, stream=True)
        else:
            response = requests.get(url, headers=headers, stream=True)
        total_size = int(response.headers.get('content-length', 0))  # Get the total file size
        if total_size >= sizelimit:
            await reply_msg.edit_text("💥That file was bigger🫠 than telegram size limitations for me🥲(2GB)")
            globals.progress_s = "File was bigger than 2GB"
            globals.run = 0
            return
        filename = url.split("/")[-1]  # Extract the filename from the URL
        if '?' in filename:
            filename = filename.split("?")[0]
        if "." not in filename:
            filename = get_file_name_from_response(response)
        if "." in filename:
            fl_list = filename.split(".")
            f_ext = fl_list.pop()
            filename_s = ".".join(fl_list)
        m_caption = f'**🔰Uploaded: {filename_s}🔗🚀\nFile-extention: {f_ext}🔑**'
        if n_name:
            try:
              n_ext=n_name.split(".").pop()
              if n_ext:
                 f_ext=n_ext
              else:
                 await reply_msg.edit_text("🔰You did'nt provide a file extention in new filename🤕 so i used my defalt as `.mp4`😑")
                 f_ext="mp4"
                 n_name=n_name+".mp4"
            except:
                await reply_msg.edit_text("🔰You did'nt provide the name correctly🤕 for rename so not renamed🙂\n\n use /help for know about it...")
                pass
            filename=n_name
            m_caption=f'**🔰Uploaded {filename_s}🔗🚀\n\nRenamed {filename_s}🪚 to {n_name}🛠\nFile-extention: {f_ext}🔑**'
        if n_caption is not None:
            m_caption = n_caption
        downloaded_size = 0
        tr_s = ''
        start_t=time.time()
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    percent = (downloaded_size / total_size) * 100
                    now_t=time.time()
                    diffr=now_t-start_t
                    globals.progress_s=f"Downloading... {percent}% of {humanbytes(total_size)}"
                    #if total_size > 0 and percent // 10 > tr_s:
                    if round(diffr % 10.00) == 0 or downloaded_size == total_size:
                       speed = downloaded_size / diffr
                       elapsed_time = round(diffr) * 1000
                       time_to_completion = round((total_size - downloaded_size) / speed) * 1000
                       estimated_total_time = elapsed_time + time_to_completion
                       elapsed_time = TimeFormatter(milliseconds=elapsed_time)
                       estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
                       progress_i = int(20 * downloaded_size / total_size)
                       progress = '[' + '✅️' * math.floor(progress_i) + '❌️' * math.floor((20 - progress_i)) + ']'
                       tmp = "{0} of {1}\nSpeed: {2}/s\nETA: {3}\n".format(
                          humanbytes(downloaded_size),
                          humanbytes(total_size),
                          humanbytes(speed),
                          # elapsed_time if elapsed_time != '' else "0 s",
                          estimated_total_time if estimated_total_time != '' else "0 s"
                       )
                       nn_s = f"🔰**Downloading!....**🔰\n\n{progress}\n\nP:{percent:.2f}%\n{tmp}"
                       if nn_s != tr_s:  #avoiding same message sending err......
                           tr_s = nn_s
                           await reply_msg.edit_text(nn_s)
        await reply_msg.edit_text(f"**🔰RVX🔰**\n\n🔰Download completed.✅️\n🔰Generating🛠 thumbnail...📸\nFor {filename}🚀")
        globals.progress_s="Download complete. Generating thumbnail..."
        thumb_path = Config.DEF_THUMB_NAIL_VID_S
        if thumb_path is None or thumb_path == "":
          thumb_path=f'{filename_s}-thumb.jpg'
          duration = 0
          with VideoFileClip(filename) as video:
              duration = int(video.duration)
              frame = video.get_frame(3.0)
              img = Image.fromarray(frame)
              img.save(thumb_path, "JPEG")
          await reply_msg.edit_text(f"**🔰RVX🔰**\n\n🔰Thumbnail generated.✅️\n🔰Trying to upload📤 it to Telegram...🚀")
          globals.progress_s=f"Thumbnail generated.\nduration detected as {duration} Uploading to Telegram..."
        start_time=time.time()
        fid = None
        if not chat_id:
            await reply_msg.reply(f"🤕Send Er:No chat_id {chat_id}")
        if not filename:
            await reply_msg.reply(f"🤕Send Er:No file {filename}")
        #await reply_msg.reply(f"Download complete. Generating thumbnail...\nchat_id:{chat_id} filename:{filename}")
        if s_type == "video":
            s_v = await reply_msg.reply_video(
               video = filename,
               duration=duration,
               caption=m_caption,
               thumb=thumb_path,
               supports_streaming=True,  # Ensure the video is streamable
               progress=progress_for_pyrogram,
               progress_args=("🔰**Uploading!...**🔰\n\n",reply_msg,start_time)
             )
            fid=s_v.video.file_id
        else:
            s_v = await reply_msg.reply_document(
               document = filename,
               caption=m_caption,
               progress=progress_for_pyrogram,
               progress_args=(
                 "🔰**Uploading!...**🔰\n\n",
                 reply_msg,
                 start_time
               )
            )
            if s_v.document:
                fid=s_v.document.file_id
            if s_v.video:
                fid=s_v.video.file_id
            if s_v.audio:
                fid=s_v.audio.file_id
        if Config.M_CHAT:
          try:
            if fid is not None:
                if s_type == "video":
                    await app.send_video(
                     chat_id=int(Config.M_CHAT),
                     video=fid,
                     caption=f"**Uploaded via RvXBot**\nBy: [{chat_id}](tg://user?id={chat_id})"
                   )
                else:
                   await app.send_video(
                     chat_id=int(Config.M_CHAT),
                     document=fid,
                     caption=f"**Uploaded via RvXBot**\nBy: [{chat_id}](tg://user?id={chat_id})"
                   )
            else:
                print("cannot find fid")
          except Exception as e:
              pass
        # Clean up the local files after uploading 
        delete_file(filename)
        delete_file(thumb_path)
        globals.progress_s = "free"
        globals.run = 0
        await reply_msg.delete()

    except Exception as e:
        await reply_msg.edit_text(f"An error occurred: {str(e)}\n\n**From RVX Uper1 system**")
        globals.progress_s=f"🤯An error occurred: {str(e)} uper1"
        print(e)
        globals.run = 0
        #delete_file(filename) #deleteing files if they downloaded...
        #delete_file(thumb_path)
