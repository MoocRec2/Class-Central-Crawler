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

url = 'https://www.classcentral.com/subject/ai'

print('Extracting Courses of Subject:', url)
print('Navigating to Page...')
driver.get(url)

row_elements = driver.find_elements_by_tag_name('tr')
print(row_elements.__len__(), 'Potential Courses')

courses = []
total_no_of_exceptions = 0

for row_element in row_elements:
    try:
        cell_elements = row_element.find_elements_by_tag_name('td')
        course_element = cell_elements[1]

        course_name = course_element.find_element_by_xpath('a/span').text
        course_link = course_element.find_elements_by_tag_name('a')[1].get_attribute('href')

        platform = course_element.find_element_by_xpath('span/a').text

        review_element = cell_elements[3].find_element_by_class_name('review-rating')

        star_tags = review_element.find_elements_by_tag_name('i')
        rating = 5
        for star_tag in star_tags:
            class_attribute = star_tag.get_attribute('class')
            if class_attribute.__contains__('icon-star-gray-light'):
                rating -= 1
            elif class_attribute.__contains__('icon-star-half'):
                rating -= 0.5

        courses.append({
            'title': course_name,
            'platform': platform,
            'rating': rating,
            'course_link': course_link
        })

    except IndexError:
        total_no_of_exceptions += 1
    except NoSuchElementException:
        total_no_of_exceptions += 1

# Filter Courses - To get only Coursera Courses
coursera_courses = []
for course in courses:
    if course['platform'] == 'Coursera':
        coursera_courses.append(course)

print('Total No. of Exceptions Occurred:', total_no_of_exceptions)
print('Courses Extracted:', courses.__len__())
print('Coursera Courses:', coursera_courses.__len__())

status = Course.upsert_courses_alt(coursera_courses)

if status:
    print('Courses have been saved to the database')
else:
    print('Error Occurred while saving to database')

driver.quit()
end_time = time.time()

time_elapsed = end_time - start_time

print('Elapsed Time:', time_elapsed, 'seconds')
