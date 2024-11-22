import os
from pyrogram import Client, filters, types
import asyncio, os, time, math, psutil
import json
from urllib.parse import urlparse
from bunkr import
from config import Config

async def ex_url(app,msg,url,chat_id=):
  ux=urlparse(url)
  nl=u.netloc
  if "bunkr" in nl:
    await ex_bunkr(app,msg,url,chat_id=chat_id)
  else:
    await msg.edit_text("Sorry cannot parse that link!")
