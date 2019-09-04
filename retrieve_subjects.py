# Retrieves all the courses of a certain subject given the URI path of the subject

import time
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import json
from json import JSONDecodeError
from db_connector import Thread
from db_connector import Course
from pprint import pprint
from selenium.webdriver.chrome.options import Options

start_time = time.time()

base_url = 'https://www.classcentral.com'

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome('C:/chromedriver', options=options)

url = 'https://www.classcentral.com'

print('Extracting Subjects:')
print('Navigating to Page...')
driver.get(url)

# subject_nav_list = driver.find_element_by_class_name('cc-navList')
# subject_nav_list = driver.find_element_by_tag_name('ul')


root_ul_tags = driver.find_elements_by_tag_name('ul')
# for root_ul_tag in root_ul_tags:
#     print('Children:', root_ul_tag.find_elements_by_class_name('cc-navList_item').__len__())

selected_ul_tag = root_ul_tags[2]
print('Selected UL Tag:', selected_ul_tag)

categories_tags = selected_ul_tag.find_elements_by_xpath('//li')
# print('Cqa', categories_tags[0].parent)

print('No. of tags:', categories_tags.__len__())

for category_tag in categories_tags:
    temp = category_tag.get_attribute('data-mega-menu-nav-list-item')

print('No. of Categories Tags:', categories_tags.__len__())

# the proper UL is the one which has 120 length
driver.quit()
quit()

exception_count = 0
links = []
subjects = []

for general_topic_tag in root_ul_tags:
    try:
        link_tag = general_topic_tag.find_element_by_tag_name('a')
        link = link_tag.get_attribute('href')
        links.append(link)
    except:
        print("Error - LINK")
    try:
        inner_tag = link_tag.find_element_by_tag_name('div')
        subject = inner_tag.text
        subjects.append(subject)
    except:
        exception_count += 1

print('UL Tag Count:', root_ul_tags.__len__())
print('No. of Exceptions:', exception_count)
print('No. of Links Extracted:', links.__len__())
print('No. of Subjects Extracted:', subjects.__len__())

driver.quit()
end_time = time.time()

time_elapsed = end_time - start_time

print('Elapsed Time:', time_elapsed, 'seconds')
