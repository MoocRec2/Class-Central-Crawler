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
from db_connector import CourseraThreads
from pprint import pprint
from selenium.webdriver.chrome.options import Options


def retrieve_thread_of_course(course):
    try:
        start_time = time.time()

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome('C:/chromedriver', options=options)

        course_url = course['course_link']
        # course_url = 'https://www.classcentral.com/course/coursera-machine-learning-835'

        course = Course.get_course({'course_link': course_url})

        driver.get(course_url)

        # ----- Course Description -----
        article_elem = driver.find_element_by_tag_name('article')
        div_elem = article_elem.find_element_by_tag_name('div')
        description = div_elem.text
        course['description'] = description

        db_operation_status = Course.upsert_courses_alt([course])
        if not db_operation_status:
            print('Additional course information could not be saved to the database')

        # ----- Reviews (Posts of Thread) -----
        review_div_elem = driver.find_element_by_id('reviews-items')
        review_items_elems = review_div_elem.find_elements_by_xpath('./div')
        print('No. of Review Items:', review_items_elems.__len__())

        reviews = []

        # TODO: Pagination

        for review_item_elem in review_items_elems:
            review = {}

            # Title

            # Content
            read_more = 0
            try:
                read_more_btn_elem = review_item_elem.find_element_by_xpath(
                    './div[@class=\'row\']/div/div[@class=\'review-content text-2 margin-vert-small\']/div/button')
                read_more_btn_elem.click()
                read_more += 1
            except NoSuchElementException:
                pass
            review_content_elem = review_item_elem.find_element_by_xpath(
                './div[@class=\'row\']/div/div[@class=\'review-content text-2 margin-vert-small\']')
            content = review_content_elem.text

            # Rating
            rating_elem = review_item_elem.find_element_by_class_name('review-rating')
            full_star_elems = rating_elem.find_elements_by_class_name('icon-star')
            half_star_elems = rating_elem.find_elements_by_class_name('icon-star-half')
            if half_star_elems.__len__() > 0:
                rating = full_star_elems.__len__() + 0.5
            else:
                rating = full_star_elems.__len__()

            review['content'] = content
            review['user'] = ''
            review['rating'] = rating

            reviews.append(review)

        # Pack Information into a single object
        thread = {'course_id': course['_id'], 'reviews': reviews}
        # thread['course_url'] = course['_id']

        db_operation_status = CourseraThreads.upsert_courses([thread])
        if not db_operation_status:
            print('Thread information could not be saved to the database')

        print('Read_more Count:', read_more)
        print('Review Length:', reviews.__len__())
        driver.quit()

        end_time = time.time()
        time_elapsed = end_time - start_time
        print('Time Elapsed:', time_elapsed)
        # pprint(course)
    except:
        print('An Error Occurred')
        print('Course:', course_url)
