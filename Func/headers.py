import json
import os

s_h = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
# Path to the headers.json file
HEADER_FILE = 'headers.json'

# Function to load headers from the JSON file
def load_headers():
    if os.path.exists(HEADER_FILE):
        with open(HEADER_FILE, 'r') as f:
            return json.load(f)
    else:
        save_headers(s_h)
        return s_h

# Function to save headers to the JSON file
def save_headers(headers):
    with open(HEADER_FILE, 'w') as f:
        json.dump(headers, f, indent=4)

# Function to get all stored headers
def get_headers():
    return load_headers()

# Function to add or update a header
def add_header(key, value):
    headers = load_headers()
    headers[key] = value
    save_headers(headers)

# Function to reset all headers (clear the file)
def reset_headers():
    if os.path.exists(HEADER_FILE):
        os.remove(HEADER_FILE)
