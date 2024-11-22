import os

class Config(object):
    
    BOT_TOKEN = os.environ.get("tk", "")
    
    API_ID = int(os.environ.get("apiid", ""))
    
    API_HASH = os.environ.get("apihash", "")
    
    download_dir = "./DOWNLOADS"
    
    MAX_FILE_SIZE = 2097152000
    
    TG_MAX_FILE_SIZE = 2097152000
    
    FREE_USER_MAX_FILE_SIZE = 2097152000
    
    CHUNK_SIZE = int(os.environ.get("chunk", 128))
    
    DEF_THUMB_NAIL_VID_S = os.environ.get("def_thumb", "")
    
    LOG_CHANNEL = int(os.environ.get("log_c", ""))

    UPDATES_CHANNEL = os.environ.get("update_c", "")
    
    OWNER_ID = int(os.environ.get("owner", ""))

    AuthUs = os.environ.get("auth","")
    
    AuthU= f"{OWNER_ID},{AuthUs}"

    M_CHAT = os.environ.get("mchat","")
    
    BOT_USERNAME = os.environ.get("bot_un", "")
