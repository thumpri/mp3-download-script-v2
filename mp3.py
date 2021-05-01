from __future__ import unicode_literals
import sys
import os
import concurrent.futures
from os import system
import youtube_dl
import getopt



class color:
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'


def get_download_path():
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'Desktop')

def print_status():
    system('cls')
    print('*** Downloading', len(URLS), 'musics ***')
    print('*** Download Directory : ', download_path , '***')
    [print(item) for item in status]


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}



def download(url):
    with youtube_dl.YoutubeDL(ydl_opts) as mp3:
        info = mp3.extract_info(url, download=False)
        title = info.get('title', None)

        color_string = color.WARNING + '[downloading]\t' + color.ENDC + title
        status[URLS.index(url)] = color_string
        print_status()

        mp3.download([url])

        color_string = color.OKGREEN + '[finished]\t' + color.ENDC + title
        status[URLS.index(url)] = color_string
        print_status()



status = []
arguments = sys.argv[1:]

try:
    options, filename = getopt.getopt(arguments, 'd:', ['dir='])

except:
    pass

download_path=get_download_path()
for option, value in options:
    if option in ['-d', '--dir']:
        download_path = value




filename =filename[0]

with open(filename, "r") as f:
    lines = f.readlines()

URLS =[]

for l in lines:
    URLS.append(l.replace('\n',''))
    

print(URLS)


for url in URLS:
    color_string = color.OKCYAN + '[starting]\t' + color.ENDC + url
    status.append(color_string)


with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(download, URLS)
