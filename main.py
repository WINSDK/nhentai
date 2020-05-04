#!/usr/bin/python3
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests
import shutil
import time
import re
import os

class handler:
    def __init__(self, ThrdID, path):
        self.ThrdID = ThrdID
        self.path   = path
        self.upload = upload

    def update(self, upload):
        self.upload              = self.ThrdID + self.upload
        DojinDir, totPage, title = self.mainPage(upload)
        self.subPage(DojinDir, totPage, title)

    @staticmethod
    def mainPage(upload):
        url = f'https://nhentai.net/g/{upload}/1'
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, "lxml")

        tit = soup.find('title')
        title = re.sub(r'-.*', "", tit.contents[0])

        info = soup.findAll('script')
        num = re.search('num_pages\":(.*)},', str(info))

        try:
            body = soup.find('section', attrs={"id": "image-container"}).findChild('img')
            dir = body['src'][:-5]
            return dir, num.group(1), title
        except:
            if title == "503 Service Temporarily Unavailable":
                print(title)
                time.sleep(2)
                return 0, 0, 0 # returns an error to retry the request
            else:
                print("Unknown Error Occurred")

    @staticmethod
    def subPage(dir, num, title):
        pagenum = 1
        try:
            os.mkdir(f'{path}/{title}')
        except:
            print("Doujinshi already downloaded")
            return
        print(f'Number of pages: {num} - Name: {title}')

        if requests.get(f'{dir}{pagenum}.jpg').status_code != 200:
            shutil.rmtree(f'{path}/{title}')
            return

        while requests.get(f'{dir}{pagenum}.jpg').status_code == 200:
            resp = requests.get(f'{dir}{pagenum}.jpg')
            with open(f'{path}/{title}/{pagenum}.jpg', 'wb') as fileout:
                fileout.write(resp.content)
            pagenum += 1

if __name__ == '__main__':
    Thrds = int(input("Input number of concurrent threads: "))
    path  = "test"
    
    if os.path.exists(path):
        print("directory Already Exists, appending current dir")
    else:
        os.mkdir(path)
    if Thrds < 1:
        raise TypeError

    pool = ThreadPoolExecutor(max_workers=Thrds*5) # Generates 5 threads per physical/virtual core
    for upload in range(1, 300000, Thrds*5):
        pool.submit(handler(Thrds, path).update(upload), upload)
    pool.shutdown