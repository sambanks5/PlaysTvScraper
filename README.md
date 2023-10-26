# PlaysTvScraper
A python web scraper for retrieving old PlaysTV clips using the Web Archive. 

PlaysTV was program that recorded highlights in games. Fairly abruptly shut down in 2019, all clips stored on their servers were deleted forever. 
I realised recently many clips were still available to view on the web archive (Wayback Machine https://web.archive.org/).
Created this small script to bring back clips from myself and friends. Ended up retrieving 80% of a total 195 videos. The other 20% were not stored on wayback machine, unfortunately lost forever.

Scraper works by loading up PlaysTV user page on Wayback Machine, firstrly retrieving source HTML using BeautifulSoup (BS4) and extracting all links.
PlaysTV used 'infinite scroll' on user pages, I had to also use Selenium Webdriver to simluate the scrolling to the bottom of the page, allowing the additional html to load and adding new video links to the list.
In the retrieved list of links, remove all those that are not 'video' links. 
Scraper then retreieves HTML source from each video page, retrieves the .mp4 from the source and downloads it to local folder. 
It will use the page 'title' as name for video file when downloaded.

