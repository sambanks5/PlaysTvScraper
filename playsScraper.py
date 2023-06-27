import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests


def main():
    ##### Web scraper using selenium for infinite scrolling page #####
    driver = webdriver.Chrome(executable_path=r"D:\PlaysTVScraper\chromedriver_win32\chromedriver.exe")
    driver.get("https://web.archive.org/web/20191211001354/http://www.plays.tv/u/theflyingnose")
    prefix = ("https://web.archive.org/web/20191211001354/")
    
    titles = []
    
    ##https://web.archive.org/web/20191210054224/http://www.plays.tv/u/calibrecoconut
    ##https://web.archive.org/web/20191210054224/

    ##https://web.archive.org/web/20191211001354/http://www.plays.tv/u/theflyingnose
    ##https://web.archive.org/web/20191211001354/

    ##https://web.archive.org/web/20191210041804/http://plays.tv/u/ryox
    ##https://web.archive.org/web/20191210041804/

    ##https://web.archive.org/web/20191210185442/https://plays.tv/u/burntmushroom
    ##https://web.archive.org/web/20191210185442/



    ## Allow x seconds for the web page to open ##
    time.sleep(1)  

    ## Lower this for quicker testing ##
    scroll_pause_time = 2.5

    ## Get the screen height ##
    screen_height = driver.execute_script("return window.screen.height;")   

    i = 1
    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break 

    ### Extract PlaysTV video URLs to list ###
    urls = []
    soup = bs(driver.page_source, "html.parser")

    ### Loop through lines of source HTML, get all lines with title class and save to urls list ###
    for parent in soup.find_all(class_="title"):
        data = parent.get('href')
        urls.append(data)

    driver.quit()
    ### Remove params and duplicates, write to test file ###
    urls = fixUrls(urls)

    ## Add the Wayback Machine prefix to the playsTV Link
    urls = addWBMPrefix(urls, prefix)

    ## Get all the '.mp4' links to source media from each link in the urls list ##
    testList = getMp4Links(urls, titles)

    fTitles = fixTitles(titles)

    finalVideoUrls = ["http:" + s for s in testList]

    downloadVideos(finalVideoUrls, fTitles)

    ## Write to test.txt file for testing ##
    f = open("test.txt", "w")
    for x in fTitles:
        f.write(x)
        f.write("\n")
    f.close()

### Remove parameters and duplicates ###
def fixUrls(urlList):
    fixedUrls = []
    fixedUrls = [url.split('?')[0] for url in urlList]
    fixedUrls = list(dict.fromkeys(fixedUrls))
    return fixedUrls

### Get rid of unnessecary details in video titles and save to list ###
def fixTitles(titles):
    uneditedTitles = titles
    titleList = []
    for x in uneditedTitles:
        try:
            found = re.search('-(.+?)-', x).group(1)
            titleList.append(found)
        except AttributeError:
            found = '' 
    return titleList

### Add Web Archive prefix to the urls 
def addWBMPrefix(urlList, prefix):
    withPrefix = [prefix + url for url in urlList]
    return withPrefix

def getMp4Links(urlList, titles):
    mp4Links = []
    x = []
    for link in urlList:
        reqs = requests.get(link)
        soup = bs(reqs.text, 'html.parser')
        try:
            x = soup.find(type="video/mp4").get('src')
        except:
            print("Dead link!")

        ## Output to terminal current video being loaded ##
        title = soup.find('title')
        print("Found and processing video: ")
        titles.append(title.string)
        print(title.string)

        mp4Links.append(x)
    return mp4Links

def downloadVideos(urlList, titles):
    for i, link in enumerate(urlList): 
        print ("Downloading file:%s"%titles[i])
 
        r = requests.get(link, stream = True)
 
        try:
            with open(titles[i] + ".mp4", 'wb') as f:
                for chunk in r.iter_content(chunk_size = 1024*1024):
                    if chunk:
                        f.write(chunk)
        except:
            "ERROR - Unable to write this file. May be due to invalid file name." 
            i - 1

        print ("%s downloaded!\n"%titles[i])
 
    print("All videos downloaded!")
    return


if __name__ == "__main__":
    main()
