# ************ A Selenium based Facebook Page Scraper ****************

# ------------------------------- Note -------------------------------

#  For searching geo-restricted pages set-up a VPN and run the script
        
#---------------------------------------------------------------------

# Library imports

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time
import csv

# Facebook credentials

USERNAME = ""
PASSWORD = ""

# Delay value. Set this a larger number when internet connection is slow

DELAY = 5

# Opening keywords CSV file

with open('keywords.csv') as f:
    reader = csv.reader(f)
    keywords = list(reader)[0]

# Setting up the chrome web driver

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

# Opening the facebook homepage

driver.get("http://www.facebook.com")

# Automated logging in

username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

username.clear()
username.send_keys(USERNAME)

password.clear()
password.send_keys(PASSWORD)

button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

print("We are logged in!")

time.sleep(DELAY)

pageLinks = []

# Code responsible for scrapping the pages

for keyword in keywords:

    # Quering the pages based on the keywords

    driver.get("https://web.facebook.com/search/pages/?q=" + keyword)

    time.sleep(DELAY)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while(True):

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(DELAY)

        anchors = driver.find_elements(By.XPATH, '//div[span[text()="Page"]]/../../../../../../div[2]/div/div/h2/span/span/span/a')

        print("Pages Fetched!")

        for a in anchors:

            link = a.get_attribute('href')

            if link not in pageLinks:

                pageLinks.append(link)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height



# Writing the scrapped page links in csv file

count = 0

with open('links.csv', 'w', newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    for i in pageLinks:
        writer.writerow((count, i))
        count += 1

print("Scrapping done!")

print("Now writing outputs to CSV file ... ")

print("This may take a while... ")

# Writing the  further info in .cs

count = 0

with open('pages.csv', 'w', newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    for i in pageLinks:

        driver.get(i)

        time.sleep(3)

        try:
            name = driver.find_element(By.XPATH, '//h2/span/span[not(@class)]').text
        except NoSuchElementException:
            name = ""

        try:
            followers = driver.find_element(By.XPATH, "//span[contains(text(), 'follow')]").text
        except NoSuchElementException:
            followers = ""

        try:
            website = driver.find_element(By.XPATH, "//a[@rel='nofollow noopener' and text() != 'Privacy Policy']").text
        except NoSuchElementException:
            website = ""
       
        try:
            about = driver.find_element(By.XPATH, '//span[text()="About"]/../../../../../../../../../../../../../div/div/div[2]/div/div/div/div/div/div/div/span/div/div/span/div/div').text
        except NoSuchElementException:
            about = ""
       
        writer.writerow((count, i, name, followers, website, about))

        count += 1

print("All done!")

    
   
        
