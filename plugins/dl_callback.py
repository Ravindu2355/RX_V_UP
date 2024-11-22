from pyrogram import Client as app
from pyrogram import filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from plugins.buttons import make_keyboard
from plugins.dl_up_1 import upload_from_url
import asyncio, os, time, requests, math, psutil
import json
from config import Config

#request for uplaod types.....
@app.on_callback_query(filters.callback_data("RVX_uper"))
async def _call_rvx(client,callback_query):
  if callback_query.message.reply_to_message:
     nkey=make_keyboard(
       [[
         {"text":"Video🎞","callback_data":"rvx_video"},{"text":"File📦","callback_data":"rvx_file"}
       ]]
     )
     reply_message_id = message.edit_text("🔰**RVX**🔰\n\nSelect the format of file you want uplaod to telegram",reply_markup=nkey)
  else:
     message.edit_text("No Url Message You send to me if you deleted it try again (send url again)")

@app.on_callback_query(filters.callback_data("ytdlp_uper"))
async def _call_ytdlp(client,callback_query):
  if callback_query.message.reply_to_message:
     nkey=make_keyboard(
       [[
         {"text":"Video🎞","callback_data":"ytd_video"},{"text":"File📦","callback_data":"ytd_file"}
       ]]
     )
     reply_message_id = message.edit_text("🔰**YTDLP**🔰\n\nSelect the format of file you want uplaod to telegram",reply_markup=nkey)
  else:
     message.edit_text("No Url Message You send to me if you deleted it try again (send url again)")


#call del with uplaod types....
@app.on_callback_query(filters.regex("rvx_"))
async def _from_rvx_dl(client,callback_query):
  dp=callback_query.data.split("_")
  msg=callback_query.message
  if dp[1]:
    if msg.reply_to_message:
      msgt=msg.reply_to_message.text
      sendtype=dp[1]
      chat_id=msg.chat.id
      if "|" in msgt:
        vars = ["url","ren","cap"]
        Values = msgt.split("|")
        variables = {}
        for var, value in zip(vars, Values):
          variables[var] = value
        await upload_from_url(client,chat_id,variables["url"],n_name=variables.get("ren",None),n_caption=variables.get("cap",None))
      else:
        url=msgt
        await upload_from_url(client,chat_id,url)
    else:
      await msg.edit_text("No url message🙃")
  else:
    await msg.edit_text("Sorry system Err:(can not recognize sending type")


@app.on_callback_query(filters.regex("ytd_"))
async def _from_ytd_dl(client,callback_query):
  await callback_query.message.edit_text("Comming soon!")
