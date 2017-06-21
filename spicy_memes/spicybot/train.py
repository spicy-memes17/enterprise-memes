import sys, requests, os, random, threading, shutil, unicodedata

header = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0",
    'Accept-Encoding': ', '.join(('gzip', 'deflate')),
    'Accept': '*/*',
    'Connection': 'keep-alive',
}

#important files/directories
IMAGES = "./images"
DESCRIPTIONS = "./descriptions"

def getData(URL):
    try:
        data = requests.get(URL, headers=header)
    except:
        data = requests.get("https://www.reddit.com/r/funny/new/", headers=header)
    
    data = unicodedata.normalize('NFKD', data.text).encode('ascii','ignore')
    return data

def getNextPage(data):
    try:
        start = 0
        start = data.find("nofollow next", start)
        while data[start] != '<':
            start -= 1
        start += 9
        end = start
        while data[end] != '"':
            end += 1
        return data[start:end]
    except:
        return "https://www.reddit.com/r/funny/new/"

def getPageTitles(data):
    l = []
    count = 0
    start = end = 0
    while count < 25:
        start = data.find("title may-blank", start)
        while data[start] != '>':
            start += 1
        start += 1
        end = start
        while data[end] != '<':
            end += 1
        l += [data[start:end]]
        count += 1
    return l

def downloadImage(URL):
    data = requests.get(URL, stream=True)
    ending = URL[-4:]
    try:
        file = open(IMAGES + "/" + str(len(os.listdir(IMAGES))) + ending, "wb")
        shutil.copyfileobj(data.raw, file)
        file.close()
    except :
        print("error while downloading image")
    
def getPageImages(data):
    img_links = []
    count = 0
    start = end = 0
    while count < 25:
        start = data.find("data-url", start)
        start += 10
        end = start
        while data[end] != '"':
            end += 1
        img_links += [data[start:end]]
        count += 1
    return img_links

#looks on number many pages on the subreddit for titles and saves them to ./descriptions in a new textfile
def trainDescriptions(number):
    file = open(DESCRIPTIONS + "/" + str(len(os.listdir(DESCRIPTIONS))) + ".txt", "w+")
    page = "https://www.reddit.com/r/funny/new/"
    count = 0

    while count != number:
        data = getData(page)
        l = getPageTitles(data)
        for i in l:
            try:
                file.write(i + '\n')
            except:
                print("Can't write this line!")
        page = getNextPage(data)
        count += 1
    file.close()

#looks on number many pages on the subreddit for images and saves them to ./images
def trainImages(number):
    page = "https://www.reddit.com/r/images/new/"
    count = 0

    while count != number:
        data = getData(page)
        links = getPageImages(data)
        links = filter(lambda x: x[-4:] == '.png' or x[-4:] == '.jpg', links)
        for link in links:
            downloadImage(link)
        page = getNextPage(data)
        count += 1