from bs4 import BeautifulSoup
import requests
import shutil
import re
import os

filepath = "target"
if os.path.exists(filepath):
    shutil.rmtree(filepath)
    os.mkdir(filepath)
else:
    os.mkdir(filepath)

def main():
    for upload in range(0, 310717): # Data value for number of doujinshi to loop through
        upload += 1
        out = mainPage(upload)
        pagenum = subPage(out[0], out[1], out[2])

def mainPage(upload):
    url = f'https://nhentai.net/g/{upload}/1'
    try:
        resp = requests.get(url)
    except OSError:
        print("Error Occurred")
        return

    soup = BeautifulSoup(resp.content, "lxml")
    tit = soup.find('title')
    title = re.sub(r'-.*', "", tit.contents[0])

    info = soup.findAll('script')
    totPage = re.split('[,.]', str(info[2]))
    
    totPage = re.search('num_pages\":(.*)}\',', str(totPage))
    body = soup.find('section', attrs={"id": "image-container"}).findChild('img')
    DojinDir = body['src'][:-5]
    return DojinDir, title, totPage.group(1)

def subPage(DojinDir, title, totPage):
    pagenum = 1
    os.mkdir(f'{filepath}/{title}')
    print(f'Number of pages: {totPage} - Name: {title}')
    
    while requests.get(f'{DojinDir}{pagenum}.jpg').status_code != 404:
        try:
            resp = requests.get(f'{DojinDir}{pagenum}.jpg')
        except OSError:
            print("Error Occurred")
            return
        
        with open(f'{filepath}/{title}/{pagenum}.jpg', 'wb') as fileout:
            fileout.write(resp.content)
        pagenum += 1
    if requests.get(f'{DojinDir}{pagenum}.jpg').status_code == 403:
        print("Error 403, Access forbidden")
        exit()

if __name__ == '__main__':
    main()
