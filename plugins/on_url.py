from pyrogram import Client as app
from pyrogram import filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from plugins.buttons import on_url_buttons, on_url_bt_text
import asyncio, os, time, requests, math, psutil
import json
from config import Config

@app.on_message(filters.private & filters.regex(pattern=".*http.*"))
async def handle_tg_ul(client, message: types.Message):
  if str(message.chat.id) in Config.AuthU:
    await message.reply_text(f"Select What You want From Below Uploaders...😎{on_url_bt_text}",reply_markup=on_url_buttons,reply_to_message_id=message.message_id)
  else:
    await message.delete()
