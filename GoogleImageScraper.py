#Google Image Search Scrapper with Google Chrome Driver
#Before starting the code you need to define the path of your own Google Chrome Driver
#Also customize the search_Url variable to your desire,For this practice projet I used the cats search url using Google Chrome
#Used libraries of python are beatifulsoup4, request, selenium and os. Make sure to download this libraries.
import bs4
import requests
from selenium import webdriver
import os
import time

#Function for the download images
def download_image(url,folder_name,num):
    reponse = requests.get(url)
    if reponse.status_code == 200:
        with open(os.path.join(folder_name,str(num)+".jpg"),'wb') as file:
            file.write(reponse.content)
    else :
        print("site is down")


#Creating a folder for the images you want to download
folder_name = 'webscrapingimages'
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)

#Defining the web driver path
chromeDriverPath = "Insert your path here"
driver = webdriver.Chrome(chromeDriverPath)

#Defining the website url that you want the scrap
search_URL = "https://www.google.com/search?q=cats&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjlntPR0Jb7AhW3QPEDHSk5B3MQ_AUoAXoECAIQAw&biw=2560&bih=1329"
driver.get(search_URL)

#Scroll to the bottom
pre_scroll_height = driver.execute_script('return document.body.scrollHeight;')
run_time, max_run_time = 0, 1
while True:
    iteration_start = time.time()
    # Scroll webpage, the 100 allows for a more 'aggressive' scroll
    driver.execute_script('window.scrollTo(0, 100*document.body.scrollHeight);')

    post_scroll_height = driver.execute_script('return document.body.scrollHeight;')

    scrolled = post_scroll_height != pre_scroll_height
    timed_out = run_time >= max_run_time

    if scrolled:
        run_time = 0
        pre_scroll_height = post_scroll_height
    elif not scrolled and not timed_out:
        run_time += time.time() - iteration_start
    elif not scrolled and timed_out:
        break

#Code that you want the start program
a = input("Waiting for user input to start...")

driver.execute_script("window.scrollTo(0,0);")
page_html = driver.page_source
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
containers = pageSoup.findAll('div',{'class':"isv-r PNCib MSM1fd BUooTd"})

#number of images
len_containers = len(containers)
#print("Found %s image containers"%(len_containers))

#Loop for clicking all the containers in the search url
for i in range(1,len_containers+1):
    if i %25 == 0:
        continue

    xPath = '//*[@id="islrg"]/div[1]/div[%s]' % (i)
    previewImageXPath = '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img' %(i)
    priviewImageElement = driver.find_element("xpath",previewImageXPath)
    previewImageURL= priviewImageElement.get_attribute("src")
    driver.find_element("xpath",xPath).click()
    timeStarted = time.time()

    while True:

        imageElement = driver.find_element("xpath",'//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img')
        imageURL  = imageElement.get_attribute('src')
        print("Waiting for full res image")

        #Controlling the full resolution image or the thumbnail image
        if imageURL != previewImageURL:
            print("Full res URL",imageURL)

            # We download the full resolution image here
            try:
                download_image(imageURL,folder_name,i)
                print("Downloaded element %s out of %s total URL %s" % (i,len_containers+1,imageURL))
            except:
                print("Cant download")
            break

        #Checking if the image is thumbnail
        else:
            currentTime = time.time()

            #if image is thumbnail and and and still cant find the full resolution image after 10 secs
            if currentTime - timeStarted > 10:
                print("Timeout!Will download a lower resolution image")
                break

