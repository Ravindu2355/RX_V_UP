from bs4 import BeautifulSoup
from config import Config
from plugins.dl_up_1 import upload_from_url
from bot import app
import globals
from pyrogram import Client, filters, types
import asyncio, os, time, math, psutil, requests
import json
from Func.headers import add_header,reset_headers
from Func.task_manager import add_task, set_tasks

dl_h = {
  "Referer": "https://bunkr.ph/"
}
def bunkr_ex_v(media_pg):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(media_pg, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    media_link = ""

    # Look for media links based on tags or attributes used by bunkrr.su
    for video_tag in soup.find_all('video'):
      if video_tag:
        video_src = video_tag.find('source')['src'] if video_tag.find('source') else video_tag['src']
        print(f'Video source URL: {video_src}')
        if video_src.startswith("http") and "bunkr" in video_src:
            media_link=video_src

    if media_link:
       return media_link
    else:
       return ""
  
def get_bunkrr_media_links(page_url):
    """Scrape media links from a Bunkrr page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(page_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    media_links = []

    # Look for media links based on tags or attributes used by bunkrr.su
    for link in soup.find_all("a", href=True):
        if link["href"].startswith("http") and "/v/" in link["href"]:
            media_links.append(link["href"])
    if media_links:
       return media_links
    else:
       return []

async def ex_bunkr(app:Client,msg:types.Message,url,chat_id=Config.M_CHAT):
  if "/v/" in url and "bunkr" in url:
    vd=bunkr_ex_v(url);
    add_header("Referer","https://bunkr.ph/")
    await upload_from_url(app, chat_id=chat_id, url=vd, reply_msg=msg)
    reset_headers()
  else:
    bls = get_bunkrr_media_links(url)
    link_l =len(bls)
    await msg.edit_text(f"🔰Extracted: {link_l} of media pages🧾")
    main_ls=[]
    erl=[]
    m_t=""
    start_time=time.time()
    for ul in bls:
      try:
        vl= await bunkr_ex_v(ul)
        if "bunkr" in vl:
           main_ls.append(vl)
        now = time.time()
        diff=now-start_time
        percent = (len(main_ls) / len(bls)) * 100
        progress_i = int(20 * len(main_ls) / len(bls))
        progress_bar = '[' + '✅️' * math.floor(progress_i) + '❌️' * math.floor((20 - progress_i)) + ']'
        prt=f"**🔰RVX🔰**\n\n**Extracting medias**\n{progress_bar}\nprogress: {percent}%\nextracted: {len(main_ls)} of {link_l}"
        if round(diff % 10.00) == 0 and m_t!=prt:
            m_t = prt
            await msg.edit_text(m_t)
        #time.sleep(1)
      except Exception as e:
        print(f"bunkr bulk link err: {e}")
        erl.append(ul)
        await msg.reply(f"Err on-Extract video sources: {e}\n try again with this link later the tasks done!🫠\nLink: {ul}")
        pass
    #add_header("Referer","https://bunkr.ph/")
    #globals.tasks[str(chat_id)]=main_ls
    set_t = set_tasks(chat_id,main_ls)
    await msg.edit_text(f"**🔰RVX🔰**\n\nAll Links Extracted from **Bunkr** ({link_l}/{len(main_ls)}) and {len(erl)} are can not extract🤕.Extracted links will be send soon🙂🙂🫡\n{set_t}")



