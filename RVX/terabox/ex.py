#Thanks Api!.....
#From https://github.com/Dapunta/TeraDL/tree/main/api

import requests
import json
from plugins.buttons import make_keyboard
from Func.simple_func import bytes_to_human_readable
api="https://teradl-api.dapuntaratya.com"
mode=1

def mfiles(data):
    result = []
    
    for item in data:
        # Add current item if it's a file (is_dir = 0)
        if item.get('is_dir') == 0:
            result.append(item)
        
        # If it's a directory (is_dir = 1), flatten its 'list' recursively
        elif item.get('is_dir') == 1:
            if 'list' in item:
                # Recursively add items from the directory's list
                result.extend(flatten_structure(item['list']))
    
    return result

def getf():
    # Define the URLs and headers
    url = 'https://www.terabox.app/wap/share/filelist?surl=GJACgid49fFsWkxtfVH3cA'
    get_file_url = f'{api}/generate_file'  # Replace 'api' with the appropriate variable
    headers = {'Content-Type': 'application/json'}
    
    # Define the data payload
    data = {
        'url': url,
        'mode': mode  # Replace 'mode' with the appropriate variable
    }
    
    # Make the POST request
    response = requests.post(get_file_url, headers=headers, json=data)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        result = response.json()  # Parse the response as JSON
        print(json.dumps(result, indent=4))  # Pretty print the JSON response
        return result
    else:
        print(f"Error: {response.status_code}")
        return None

def dlg(uk, sid, ts, sign, jt, c, fid):
    # Define the parameters for the request
    param = {
      'mode'      : mode,
      'uk'        : uk,
      'shareid'   : sid,
      'timestamp' : ts,
      'sign'      : sign,
      'js_token'  : jt,
      'cookie'    : c,
      'fs_id'     : fid
    }
    get_link_url = f"{api}/generate_link"  # Replace 'api' with the appropriate URL
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(param)  # Convert the param to JSON format
    response = requests.post(get_link_url, headers=headers, data=data)
    if response.status_code == 200:
        result = response.json()  # Parse the response as JSON
        print(json.dumps(result, indent=2))  # Pretty print the JSON response
        return result
    else:
        print(f"Error: {response.status_code}")
        return None

async def tera(app, msg, url, chat_id):
  tx=getf(url)
  if tx:
    if tx['list']:
      flist= mfiles(tx['list'])
      for fi in flist:
        if fi['is_dir'] == 0 or fi['is_dir'] == "0":
          dls = await dlg(tx['uk'], tx['shareid'], tx['timestamp'], tx['sign'], tx['js_token'], tx['cookie'], file)
          if dls and dls["status"] == "success":
            if dls["download_link"]:
              keys=[]
              for k in dls["download_link"]:
                bs = [{"text":k,"url":dls["download_link"][k]}]
                keys.append(ns)
              kboard = make_keyboard(keys)
              await msg.reply_photo(
                photo=fi['image'],
                caption=f"**🔰RVX🔰**\n\nName: {fi['name']}\nType: {fi['type']}\nSize: {bytes_to_human_readable(fi['size'])}",
                reply_markup=kboard
              )
              time.sleep(2)
            else:
              await msg.edit_text("Sorry I cannot extract dl links for that🥲")
          else:
            await msg.edit_text("Err on File Extractor!...")
        else:
          await msg.edit_text("File Ex err")
    else:
      await msg.edit_text("Sorry i cant recognize files!")
  else:
    await msg.edit_text("Sorry RVX-Terabox section on err🤕")