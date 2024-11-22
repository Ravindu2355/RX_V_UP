import os
from pyrogram import Client, filters, types
import asyncio, os, time, math, psutil
import json
from urllib.parse import urlparse
from RVX.bunkr import ex_bunkr
from config import Config

async def ex_url(app,msg,url,chat_id=Config.M_CHAT):
  ux=urlparse(url)
  nl=ux.netloc
  if "bunkr" in nl:
    await ex_bunkr(app,msg,url,chat_id=chat_id)
  else:
    await msg.edit_text("Sorry cannot parse that link!")
