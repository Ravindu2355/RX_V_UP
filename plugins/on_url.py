from pyrogram import Client, filters, types
from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.buttons import on_url_buttons, on_url_bt_text
import asyncio, os, time, requests, math, psutil
import json
from config import Config

@app.on_message(filters.private & filters.regex(pattern=".*http.*"))
async def handle_tg_ul(client, message: types.Message):
  if message.chat.id in Config.AuthU:
    await message.reply(f"Select What You want From Below Uploaders...😎{on_url_bt_text}",reply_markup=on_url_buttons)
  else:
    await message.delete()
