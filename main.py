import time
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
import json
from json import JSONDecodeError
from db_connector import Thread
from pprint import pprint
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
driver = webdriver.Chrome('C:/chromedriver', options=options)

driver.get('https://www.classcentral.com/')

form = driver.find_element_by_tag_name('form')

input_elements = driver.find_elements_by_tag_name('input')
search_input = input_elements[0]
btn_input = input_elements[1]

search_input.send_keys('qwe')

# driver.quit()
