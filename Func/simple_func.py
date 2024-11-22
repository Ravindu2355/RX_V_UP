import os

def delete_file_if_exists(file_path):
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
