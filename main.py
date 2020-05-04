from bs4 import BeautifulSoup
import concurrent.futures
import requests
import shutil
import time
import re
import os

class handler:
    def __init__(self, ThrdID, upload, path):
        self.ThrdID = ThrdID
        self.upload = upload
        self.path   = path

    def update(self):
        self.upload              = self.ThrdID + self.upload
        DojinDir, totPage, title = self.mainPage()
        self.subPage(DojinDir, totPage, title)

    def mainPage(self):
        url = f'https://nhentai.net/g/{self.upload}/1'
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, "lxml")

        tit = soup.find('title')
        title = re.sub(r'-.*', "", tit.contents[0])

        info = soup.findAll('script')
        totPage = re.search('num_pages\":(.*)},', str(info))

        try:
            body = soup.find('section', attrs={"id": "image-container"}).findChild('img')
            DojinDir = body['src'][:-5]
            return DojinDir, totPage.group(1), title
        except:
            if title == "503 Service Temporarily Unavailable":
                time.sleep(2)
                print(title)
            else:
                print("Unknown Error Occurred")
            return 

    def subPage(self, DojinDir, totPage, title):
        pagenum = 1
        try:
            os.mkdir(f'{self.path}/{title}')
        except:
            print("Doujinshi already downloaded")
            return
        print(f'Number of pages: {totPage} - Name: {title}')

        if requests.get(f'{DojinDir}{pagenum}.jpg').status_code != 200:
            print(f'Some generic error occurred. - {DojinDir}')
            shutil.rmtree(f'{self.path}/{title}')
            return

        while requests.get(f'{DojinDir}{pagenum}.jpg').status_code == 200:
            resp = requests.get(f'{DojinDir}{pagenum}.jpg')
            with open(f'{self.path}/{title}/{pagenum}.jpg', 'wb') as fileout:
                fileout.write(resp.content)
            pagenum += 1

if __name__ == '__main__':
    Thrds = int(input("Input number of concurrent threads: "))
    path  = "test"
    
    if os.path.exists(path):
        print("Directory Already Exists, appending current Dir")
    else:
        os.mkdir(path)
    if Thrds < 1:
        raise TypeError

    for upload in range(1, 300000, Thrds): # Data value for number of doujinshi to loop through
        with concurrent.futures.ThreadPoolExecutor(max_workers=Thrds-1) as executor:
            for index in range(Thrds):
                handle = handler(index, upload, path)
                executor.submit(handle.update())
