from __future__ import unicode_literals
from bs4 import BeautifulSoup
import urllib.request
import youtube_dl
import requests
import time
import math
import os

channelURL = 'https://www.youtube.com/channel/UCR4z8ccOWNoUThB4VAMNBTg/videos'
# channelURL = 'https://www.youtube.com/channel/UCPLE-tmCc2KRvFZeUNB30sg'  # Deepak

while True:

    os.system('cls')
    ######################## BeautifulSoup ########################

    # Scrapping
    print('Downloading webpage')
    response = requests.get(channelURL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Finding the first video in the list
    latestVideo = 'https://www.youtube.com' + \
        soup.select('a[aria-describedby]')[0]['href']

    ######################## Youtube-dl ########################

    meta = {}
    currDownload = ''

    # Printing Head
    def printHeader():
        os.system('cls')
        print('######################################### META INFO #########################################')
        print('  id          :', meta['id'])
        print('  title       :', meta['title'])
        print('  upload date :', meta['upload_date'])
        print('  uploader    :', meta['uploader'])
        print('  duration    :', meta['duration'])
        # print('  views       :', meta['view_count'])
        # print('  likes       :', meta['like_count'])
        # print('  dislikes    :', meta['dislike_count'])
        # print('  format      :', meta['format'])
        print('#############################################################################################')

    # Print Progress
    def progress(per, speed, total, eta):
        printHeader()
        perF = math.floor(float(per[:-1])/2)
        print('|', '█'*perF, ' '*(50-perF), '|', sep='', end='')
        print(per + ' of ~' + total + ' at ' + speed + ' ETA ', eta)

    # Logger
    class MyLogger(object):
        def debug(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            # print(msg)
            pass

    # Hook
    def my_hook(d):
        if d['status'] == 'downloading':
            progress(d['_percent_str'], d['_speed_str'],
                     d['_total_bytes_estimate_str'], d['_eta_str'])
        if d['status'] == 'finished':
            print('Finished Downloading, now converting...')
            f = open('lastVideo.txt', 'w')
            f.write(currDownload)
            f.close()

    # Youtube-dl Options
    ydl_opts = {
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }

    # Download
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(latestVideo, download=False)

        f = open('lastVideo.txt', 'r')
        lastDownload = f.read()
        f.close()

        if(meta['id'] == lastDownload):
            secondsToCheck = 1800
            for i in range(secondsToCheck):
                rem = secondsToCheck - i
                os.system('cls')
                print("Video already downloaded")
                print("Channel will be checked again in",
                      math.floor(rem/60), 'mins,', rem % 60, 'secs')
                time.sleep(1)
        else:
            currDownload = meta['id']
            ydl.download([latestVideo])
