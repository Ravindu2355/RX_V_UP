import os
from pyrogram import Client, filters, types
import asyncio, os, time, math, psutil
import json
from urllib.parse import urlparse
from RVX.bunkr.ex import ex_bunkr
from RVX.terabox.ex import tera
from config import Config

async def ex_url(app,msg,url,chat_id=Config.M_CHAT):
  await msg.edit_text("🔰Processing!....🚀")
  if "bunkr" in url:
    await ex_bunkr(app,msg,url,chat_id=chat_id)
  elif "tera" in url:
    await tera(app, msg, url, chat_id=chat_id)
  else:
    await msg.edit_text("Sorry cannot parse that link!🤕")
