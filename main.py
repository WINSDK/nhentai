from bs4 import BeautifulSoup
import requests
import shutil
import time
import re
import os

filepath = "target"

if os.path.exists(filepath):
    #shutil.rmtree(filepath)
    #os.mkdir(filepath)
    print("Directory Already Exists, appending current Dir")
else:
    os.mkdir(filepath)

def main():
    for upload in range(1, 310717): # Data value for number of doujinshi to loop through
        upload += 1
        out = mainPage(upload)
        if out[1] != 0:
            pagenum = subPage(out[0], out[1], out[2])
        else:
            time.sleep(3)
            pass

def mainPage(upload):
    url = f'https://nhentai.net/g/{upload}/1'
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
        print(title)
        Success = 0
        return title, Success

def subPage(DojinDir, totPage, title):
    pagenum = 1

    try:
        os.mkdir(f'{filepath}/{title}')
    except:
        print("Doujinshi already downloaded")
        pagenum += 1
        return
    print(f'Number of pages: {totPage} - Name: {title}')

    while requests.get(f'{DojinDir}{pagenum}.jpg').status_code == 200:
        resp = requests.get(f'{DojinDir}{pagenum}.jpg')
        with open(f'{filepath}/{title}/{pagenum}.jpg', 'wb') as fileout:
            fileout.write(resp.content)
        pagenum += 1
        
    if requests.get(f'{DojinDir}{pagenum}.jpg').status_code == 404 or 403:
        print(f'Some generic error occurred. - g/{pagenum}/')
        shutil.rmtree(f'{filepath}/{title}')

if __name__ == '__main__':
    main()
