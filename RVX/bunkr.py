from bs4 import BeautifulSoup
from config import Config
from plugins.dl_up_1 import upload_from_url
from bot import app
import globals
from pyrogram import Client, filters, types
import asyncio, os, time, math, psutil, requests
import json
from Func.headers import add_header,reset_headers

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
    media_links = []

    # Look for media links based on tags or attributes used by bunkrr.su
    for video_tag in soup.find_all('video'):
      if video_tag:
        video_src = video_tag.find('source')['src'] if video_tag.find('source') else video_tag['src']
        print(f'Video source URL: {video_src}')
        if video_src.startswith("http") and "/v/" in video_src:
            media_link=src

    return media_link
  
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

    return media_links

async def ex_bunkr(app:Client,msg:types.Message,url,chat_id=Config.M_CHAT):
  if "/v/" in url and "bunkr" in url:
    vd=bunkr_ex_v(url);
    add_header("Referer","https://bunkr.ph/")
    await upload_from_url(app, chat_id, video)
    reset_headers()
  else:
    bls = get_bunkrr_media_links(url)
    link_l =len(bls)
    await msg.edit_text(f"Extracted: {link_l} of media pages")
    main_ls=[]
    start_time=time.time()
    for ul in bls:
      vl= bunkr_ex_v(ul)
      if "bunkr" in vl:
         main_ls.append(vl)
      now = time.time()
      diff=now-star_time
      if round(diff % 10.00) == 0:
        await msg.edit_text(f"extracted {len(main_ls)} of {link_l}")
    globals.tasks[str(chat_id)]=main_ls
    msg.edit_text(f"All Links Extracted ({link_l}/{len(main_ls)}) and they will be send soon🙂🙂🫡")



