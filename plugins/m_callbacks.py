from pyrogram import Client as app
from pyrogram import filters, types
from Func.reply_text import Text

@app.on_callback_query(filters.regex("^delm$"))
async def _cancel(client,callback_query):
  await callback_query.message.delete()

@app.on_callback_query(filters.regex("^home$"))
async def _home(client,callback_query):
  message=callback_query.message
  if str(message.chat.id) in AuthU:
        un=message.chat.username
        st=Text.start
        if un:
            nun=un
        else:
            nun=message.chat.first_name
        if nun:
          st=st.replace("R-user",nun)
        st=st.replace("user_id",str(message.chat.id))
        reply_msg = await message.edit_text(st)
  else:
        await message.delete();

@app.on_callback_query(filters.regex("^help$"))
async def _chelp(client,callback_query):
  await callback_query.message.edit_text(Text.help)
