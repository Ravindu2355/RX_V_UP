#for direct link upload.....(uploader rvx direct)
from pyrogram import Client, filters, types
import asyncio, os, time, requests, math, psutil, json
from moviepy.editor import VideoFileClip
from PIL import Image
from Func.display_progress import progress_for_pyrogram, humanbytes, TimeFormatter
from Func.cookie import r_cookies, w_cookies, clear_cookies
from Func.simple_func import delete_file
import globals

async def upload_from_url(client: Client, chat_id:str, url: str, n_caption=None):
    global progress_s
    reply_msg = await app.send_message(chat_id=chat_id,text="Processing!....")
    globals.progress_s="Processing...!"
    try:
        if len(url) < 2:
            await reply_msg.edit_text("Please provide a URL!")
            globals.progress_s="free"
            globals.run = 0
            return
        await reply_msg.edit_text("Starting download...")
        globals.progress_s="Download starting...."
        cookies = r_cookies()
        if not cookies:
            response = requests.get(url, cookies=cookies, stream=True)
        else:
            response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))  # Get the total file size
        if total_size >= sizelimit:
            await reply_msg.edit_text("That file was bigger than telegram size limitations for me🥲")
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
        m_caption = f'Uploaded: {filename_s}\n file-extention: {f_ext}'
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
                       nn_s = f"Downloading: {progress}\n\nP:{percent:.2f}%\n{tmp}"
                       if nn_s != tr_s:  #avoiding same message sending err......
                           tr_s = nn_s
                           await reply_msg.edit_text(nn_s)
        await reply_msg.edit_text("Download complete. Generating thumbnail...")
        globals.progress_s="Download complete. Generating thumbnail..."
        thumb_path=f'{filename_s}-thumb.jpg'
        duration = 0
        with VideoFileClip(filename) as video:
              duration = int(video.duration)
              frame = video.get_frame(3.0)
              img = Image.fromarray(frame)
              img.save(thumb_path, "JPEG")
        await reply_msg.edit(f"Thumbnail generated.\nduration detected as {duration} Uploading to Telegram...")
        globals.progress_s=f"Thumbnail generated.\nduration detected as {duration} Uploading to Telegram..."
        start_time=time.time()
        s_v = await app.send_video(
               chat_id = int(chat_id),
               video = filename,
               duration=duration,
               caption=m_caption,
               thumb=thumb_path,
               supports_streaming=True,  # Ensure the video is streamable
               progress=progress_for_pyrogram,
               progress_args=(
                "uploading!",
                 reply_msg,
                 start_time
              )
             )
        fid=s_v.video.file_id
        try:
          await app.send_video(
            chat_id=int(M_CHAT),
            video=fid,
            caption=f"**Uploaded via RvXBot**"
          )
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
        globals.progress_s=f"An error occurred: {str(e)} uper1"
        print(e)
        globals.run = 0
        delete_file(filename) #deleteing files if they downloaded...
        delete_file(thumb_path)
