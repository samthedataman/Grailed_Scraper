#import nessicary packages
import selenium 
from selenium import webdriver
import pandas as pd
import numpy as np
import requests as r
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import time
from selenium.common.exceptions import NoSuchElementException        
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException

import json
import datetime as dt 
from datetime import date,datetime,timedelta
from selenium.webdriver.chrome.options import Options
options = Options()
options.page_load_strategy = 'normal'
# options.add_argument("--remote-debugging-port=9230")
TODAY = dt.datetime.now().strftime("%m%d")

#create empy attribute list of desirable scraping elements off of grailed.com
designer_cat = []
size_list = []
color = []
price = []
size = []
title = []
brand =[]
condition = []
shipping_from = []
seller_name = []
seller_transactions = []
seller_feedback = []
seller_listings = []
shipping_cost =[]
like_amount = []
number_of_photos =  []
price = []
new_price = []
seller_name= []
seller_transactions = []
seller_rating = []
seller_feedback =[]
item_description =[]
seller_listings = []
likes = []
shipping_cost = []
#open chrome driver on your machine
driver = webdriver.Chrome('/Users/samsavage/Downloads/chromedriver',options=options)
driver.quit()
driver = webdriver.Chrome('/Users/samsavage/Downloads/chromedriver',options=options)



#category list that can be iterated through if you would like to scrape multiple categories
cat_list = ['https://www.grailed.com/categories/outerwear','https://www.grailed.com/categories/footwear',
'https://www.grailed.com/categories/tops','https://www.grailed.com/categories/bottoms','https://www.grailed.com/categories/accessories']
#In this scraper example a single test link will be used (this link is for patagonia nano puff jackets)
test_list = ['https://www.grailed.com/shop/qGyKkEMjTw']
#create empy link list 
links_list = []  
#retrive data from test_list
for categories in test_list:
#activate driver to get patagonia nano puff jackets from grailed
    driver.get(categories)
#sleep 2 seconds between each iteration to mimic user    
    time.sleep(2)
#listing_count = the count of elements on the page   
    listing_count = driver.find_element_by_xpath("//*[@id='shop']/div/div/div[1]/div[1]").get_attribute("textContent")
#retreive only numbers from listing count element and turn into integer
    listing_count = [i for i in listing_count if i.isdigit()]
    listing_count  = ''.join(map(str, listing_count ))
    listing_count = int(listing_count)
    print(f'scraping for {listing_count} listings')
#B/c grailed.com uses infinite scroll we need to scroll through each page until we hit the end of the page, since there are about 30 items per page we want to scroll from 0 to max(items)/30
    #approx 20 items per scroll 
    DIVISOR = 80
    for page in range(0,(listing_count//DIVISOR)+1):
        ele = page+1
        print(f'scrolling though page {ele} of {(listing_count//DIVISOR)+1}')
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")       
        print(f'scrolling @ {round(ele/(listing_count//DIVISOR+1),4)}% completed')
        time.sleep(2)
#Break loop after we have completed the final scroll and retreive all links for products on the page
    links = driver.find_elements_by_class_name("listing-item-link")
#append links to the links_list and retreive the ahref's {links} attributes
    for link in links:
        try:
            links_list.append(link.get_attribute("href"))
        except selenium.common.exceptions.WebDriverException:
            continue
#write links to file for safekeeping
    with open (f'/Users/samsavage/Desktop/Grailed_Scraper/{TODAY}_full_data_grailed.txt','w') as file:
        file.write(json.dumps(links_list))


#print number of links scraped, should match the origonal listing number retrieved
print(f'scraper as found {len(set(links_list))} unique listings')
#set and index = 0
index = 0
#iterate through each link and grab each data element of importance
for clothing_item in list(set(links_list)):
    try:
        index += 1
#print a % of data completed {this is useful for large pages of links}
        print(f"{round(index/len(set(links_list)),4)*100}% of data downloaded")
        driver = webdriver.Chrome('/Users/samsavage/Downloads/chromedriver',options=options)
        categories = categories.rsplit('/', 1)[-1]
        clothing_type_master = []
        clothing_type_master.append(categories)
        try:
            driver.get(clothing_item)
        except WebDriverException as e:
            print(e)
            continue
        try:
            description = driver.find_element_by_xpath("//*[@id='__next']/div/main/div[1]/div[1]/div[2]/div[1]/div[2]/p[1]").get_attribute("textContent")
        except (WebDriverException,NoSuchElementException) as e:
            print(e)
            continue
        description = description.replace("×",',')
        designer_cat.append(description)
        try:
            size = driver.find_element_by_xpath("//*[@id='__next']/div/main/div[1]/div[1]/div[2]/div[1]/div[2]/p[3]").get_attribute("textContent")
        except (WebDriverException,NoSuchElementException) as e:
            print(e)
            continue
        
        size_list.append(size)
        try:
            title_driver = driver.find_element_by_xpath("//*[@id='__next']/div/main/div[1]/div[1]/div[2]/div[1]/div[2]/p[2]").get_attribute("textContent")
        except (WebDriverException,NoSuchElementException) as e:
            print(e)
            continue
        title.append(title_driver)
        try:
            color_driver = driver.find_element_by_xpath("//*[@id='__next']/div/main/div[1]/div[1]/div[2]/div[1]/div[2]/p[4]").get_attribute("textContent")
        except (WebDriverException,NoSuchElementException) as e:
            print(e)
            continue
        color.append(color_driver)
        try:
            condition_driver = driver.find_element_by_xpath("//*[@id='__next']/div/main/div[1]/div[1]/div[2]/div[1]/div[2]/p[5]").get_attribute("textContent")
        except (WebDriverException,NoSuchElementException) as e:
            print(e)
            continue
        condition.append(condition_driver)
        try:
            price_driver = driver.find_element_by_xpath("//*[@id='__next']/div/main/div[1]/div[1]/div[2]/div[1]/div[3]/span").get_attribute("textContent")
        except (WebDriverException,NoSuchElementException) as e:
            print(e)
            continue
        price.append(price_driver)
        try:
            new_price_driver = driver.find_element_by_xpath("//*[@id='__next']/div/main/div[1]/div[1]/div[2]/div[1]/div[3]/span[1]").get_attribute("textContent")
        except (WebDriverException,NoSuchElementException) as e:
            print(e)
            continue
        new_price.append(new_price_driver) 
        try:
            seller_name_driver =  driver.find_element_by_xpath("//*[@id='__next']/div/main/div[1]/div[1]/div[2]/div[2]/div[2]/span").get_attribute("innerText")
        except (WebDriverException,NoSuchElementException) as e:
            print(e)
            continue
        seller_name.append(seller_name_driver)
        try:
            seller_transactions_driver = driver.find_element_by_xpath("//*[@id='__next']/div/main/div[1]/div[1]/div[2]/div[2]/div[2]/span/a/span[2]").get_attribute("innerText")
        except (WebDriverException,NoSuchElementException) as e:
            print(e)
            continue        
        seller_transactions.append(seller_transactions_driver)
        try:
            seller_feedback_driver = driver.find_element_by_xpath("//*[@id='__next']/div/main/div[1]/div[1]/div[2]/div[2]/div[2]/a[1]/span").get_attribute("innerText")
        except (WebDriverException,NoSuchElementException) as e:
            print(e)
            continue        
        seller_feedback.append(seller_feedback_driver)
        try:
            seller_listings_driver = driver.find_element_by_xpath("//*[@id='__next']/div/main/div[1]/div[1]/div[2]/div[2]/div[2]/a[2]").get_attribute("innerText")
        except (WebDriverException,NoSuchElementException) as e:
            print(e)
            continue        
        seller_listings.append(seller_listings_driver)
        try:
            shipping_cost_driver = driver.find_element_by_xpath("//*[@id='__next']/div/main/div[1]/div[1]/div[2]/div[1]/div[4]/span/strong").get_attribute("innerText")
        except (WebDriverException,NoSuchElementException) as e:
            print(e)
            continue        
        shipping_cost.append(shipping_cost_driver)
        try:
            item_description_driver = driver.find_element_by_xpath("//*[@id='__next']/div/main/div[1]/div[1]/div[2]/div[4]/div").get_attribute("innerText")                                 
        except (WebDriverException,NoSuchElementException) as e:
            print(e)
            continue        
        item_description.append(item_description_driver)
        try:        
            likes_driver = driver.find_element_by_xpath("//*[@id='__next']/div/main/div[1]/div[1]/div[2]/div[1]/button/span").get_attribute("innerHTML")
        except (WebDriverException,NoSuchElementException) as e:
            print(e)
            continue            
        likes.append(likes_driver)
        try:
            shipping_from = driver.find_element_by_xpath("//*[@id='__next']/div/main/div[1]/div[1]/div[2]/div[1]/div[4]/span/strong/[1]").get_attribute("innerHTML")                                            
        except (WebDriverException,NoSuchElementException) as e:
            print(e)
            continue        
        driver.quit()  
    except NoSuchElementException:
        continue
    driver.close()
                
    
    #compress all lists created into a dictionary
grailed_dictionary = dict(zip([
"designer_cat",
"clothing_type_master",
"size_list",
"color",
"price",
"title",
"condition",
"shipping_from",
"seller_name",
"seller_transactions",
"seller_feedback",
"seller_listings",
"like_amount",
"number_of_photos",
"price",
"new_price",
"seller_name",
"seller_transactions",
"seller_rating",
"seller_feedback",
"item_description",
"seller_listings",
"likes",
"shipping_cost"],
[designer_cat,
clothing_type_master,
size_list,
color,
price,
title,
condition,
shipping_from,
seller_name,
seller_transactions,
seller_feedback,
seller_listings,
like_amount,
number_of_photos,
price,
new_price,
seller_name,
seller_transactions,
seller_rating,
seller_feedback,
item_description,
seller_listings,
likes,
shipping_cost]))
#turn dictionary into a dataframe and transpose to show tabular format
grail_dataframe = pd.DataFrame.from_dict(grailed_dictionary,orient='index').transpose()
#clean dataframe
#write the dataframe a to a csv 
grail_dataframe.to_csv(f"~/Desktop/Grailed_Scraper/{TODAY}_data_grailed.csv")
time.sleep(3)

print("data frame written")

    
    # df = grail_dataframe.copy()
