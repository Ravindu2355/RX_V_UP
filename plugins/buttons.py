from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def make_keyboard(X):
    keyboard = [
        [
            InlineKeyboardButton(button.get("text"), callback_data=button.get("callback_data") or button.get("url"))
            for button in row
        ]
        for row in X
    ]
    
    return InlineKeyboardMarkup(keyboard)

on_url_buttons = make_keyboard(
  [
    [{"text":"🚀RVX Uploader💪","callback_data":"RVX_uper"}],
    [{"text":"🔰Yt-dlp🔰","callback_data":"ytdlp_uper"}],
    [{"text":"💯RVX-Extr💥","callback_data":"RVX_Ex"}]
  ]
)
on_url_bt_text = "\n\n🔰**RVX Uploader**:for upload only direct links\n🔰**Yt-dlp**: For eny upload but slow and some time giving errors"

v_or_f = make_keyboard(
    [
        [
            {"text":"Video","callback_data":"as_video"},
            {"text":"File","callback_data":"as_file"}
        ]
    ]
)
