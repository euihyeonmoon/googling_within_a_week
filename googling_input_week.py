from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

import datetime
from datetime import date, timedelta

link_list = []
title_list = []
summary_list = []
date_list = []

key = input("최근 1주 Google News 검색: ")
url = 'https://www.google.com/search?q=' + key +'&tbm=nws&tbs=qdr:w'

def chroming(url):
    global options
    global driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    driver.get(url)

# crawl the data from google using selenium with Chrome
def google_crawl():
    time.sleep(2)
    # get the title
    title = driver.find_elements_by_css_selector(".mCBkyc.tNxQIb.ynAwRc.JIFdL.JQe2Ld.nDgy9d")
    for _ in title:
        title_list.append(_.text)
    # get the summary
    summary = driver.find_elements_by_css_selector('.GI74Re.nDgy9d')
    for _ in summary:
        summary_list.append(_.text)
    # get the date
    date = driver.find_elements_by_css_selector('.S1FAPd.OSrXXb.ecEXdc')
    for _ in date:
        date_list.append(_.text)
    #get the link
    link = driver.find_elements_by_css_selector('.WlydOe')
    for _ in link:
        print(_.get_attribute('href'))
        link_list.append(_.get_attribute('href'))
        
    print('Crawling...')

    # click the next page
    next_button = driver.find_elements_by_css_selector('.SJajHc.NVbCr')
    next_button = next_button[-1]
    next_button.click()
    time.sleep(5)
    return title_list, summary_list, date_list, link_list

def Chroming_end():
    driver.close()

chroming(url)
try:
    for _ in range(1, 5):
        title_list, summary_list, date_list, link_list = google_crawl()
        Chroming_end()
except:
    pass
print(len(title_list))
print(len(summary_list))
print(len(date_list))
print(len(link_list))

today = date.today().strftime("%Y-%m-%d")
data = pd.DataFrame({'Title':title_list, 'Summary':summary_list, 'Date':date_list,
                     'Link':link_list})
print(data)
data.to_excel(key + ' ' + 'NEWS' + ' ' + today + '.xlsx', index=False)

print("Crawling is Done")