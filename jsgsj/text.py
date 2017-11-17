#!python
# encoding: utf-8
import os
from urllib.request import urlopen
 
from bs4 import BeautifulSoup
 
 
def get(url):
    response = urlopen(url)
    html = response.read().decode("gbk")
    response.close()
    return html
 
 
def detect(html):
    soup = BeautifulSoup(html, "html.parser")
    images = soup.select("img[data-lazyload-src]")
    return images
 
 
def download(url, pic_path):
    response = urlopen(url)
    img_bytes = response.read()
    f = open(pic_path, "wb")
    f.write(img_bytes)
    f.close()
 
 
def main():
    html = get("http://pp.163.com/longer-yowoo/pp/10069141.html")
    images = detect(html)
    pic_folder = "/pics"
    os.mkdir(pic_folder)
    for i in range(len(images)):
        url = images[i].attrs['data-lazyload-src']
        download(url, pic_folder + "/" + str(i) + ".jpg")
 
 
if __name__ == '__main__':
    main()