import os

def bytes_to_human_readable(byte_count):
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    i = 0
    while byte_count >= 1024 and i < len(units) - 1:
        byte_count /= 1024.0
        i += 1
    return f"{byte_count:.1f}{units[i]}"

def delete_file(file_path):
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted.")
            return True
        except Exception as e:
            print(f"Error deleting file '{file_path}': {e}")
            return False
    else:
        print(f"File '{file_path}' does not exist.")
        return False

def get_file_name_from_response(response):
    # Check if Content-Disposition header is present
    content_disposition = response.headers.get('Content-Disposition')
    if content_disposition:
        # Extract the filename from the Content-Disposition header
        filename_part = content_disposition.split('filename=')[-1]
        filename = filename_part.strip(' "')
        return filename
    
    # Fallback to extracting the file name from the URL
    return f"video_{str(time.time())}.mp4"
    
def intt(value):
    if isinstance(value, int):
        return value
    else:
        try:
            return int(value)
        except ValueError:
            print(f"Cannot convert {value} to an integer.")
            return None  # Return None or handle the error as needed

video_ext = ["mp4", "mkv", "avi", "mov", "flv", "wmv", "webm", "mpeg", "mpg", "3gp", "ts", "vob", "ogv", "ogx", "m4v", "f4v", "rm", "rmvb", "asf", "divx", "xvid", "svq3", "qt", "amv", "gifv"]
