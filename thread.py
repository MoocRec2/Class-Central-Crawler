import time
from selenium import webdriver
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
from db_connector import CourseAlt
from db_connector import CourseraThreads
from pprint import pprint
from selenium.webdriver.chrome.options import Options
import copy
import urllib.parse


def retrieve_thread_of_course(course):
    # try:
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
    try:

        article_elem = driver.find_element_by_tag_name('article')
    except:
        print('Error Occurred - Article')
        temp_course = copy.deepcopy(course)
        temp_course.pop('_id', 'qwe')
        temp_course['error'] = 'article'
        db_operation_status = CourseAlt.upsert_courses([temp_course])
        if not db_operation_status:
            print('UNABLE to Mark in DB')
        return
    div_elem = article_elem.find_element_by_tag_name('div')
    description = div_elem.text
    course['description'] = description
    # CourseAlt.upsert_courses([course])
    temp_course = copy.deepcopy(course)
    temp_course.pop('_id', 'qwe')
    db_operation_status = CourseAlt.upsert_courses([temp_course])
    if not db_operation_status:
        print('Additional course information could not be saved to the database')
    else:
        print(description)
        print('INSERTED')

    # TODO: Picture

    #  Proper URL
    wrapper_div_elem = driver.find_element_by_xpath(
        '//div[@class=\'col width-2-3 xlarge-up-width-3-5 xxlarge-up-width-2-3 padding-left-small\']')
    proper_url = wrapper_div_elem.find_element_by_tag_name('a').get_attribute('href')
    # TODO: Extract URL
    components = proper_url.split('&')
    proper_url = components[5]
    proper_url = proper_url.split('=')[1]
    proper_url = urllib.parse.unquote(proper_url)
    # print(proper_url)
    # quit()

    temp_course = copy.deepcopy(course)
    temp_course.pop('_id', 'qwe')
    temp_course['proper_url'] = proper_url
    temp_course['link_fixed'] = True
    db_operation_status = CourseAlt.upsert_courses([temp_course])
    if not db_operation_status:
        print('UNABLE to Save Proper URL in DB')

    # ----- Reviews (Posts of Thread) -----
    try:
        review_div_elem = driver.find_element_by_id('reviews-items')
    except NoSuchElementException:
        print('Error Occurred - Review-Items Not Present')
        temp_course = copy.deepcopy(course)
        temp_course.pop('_id', 'qwe')
        temp_course['error'] = 'review_items'
        db_operation_status = CourseAlt.upsert_courses([temp_course])
        if not db_operation_status:
            print('UNABLE to Mark in DB')
        return
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
            while True:
                try:
                    read_more_btn_elem.click()
                    break
                except:
                    pass
            read_more += 1
            review_content_elem = review_item_elem.find_element_by_xpath(
                './div[@class=\'row\']/div/div[@class=\'review-content text-2 margin-vert-small\']')
            content = review_content_elem.text
        except NoSuchElementException:
            print('Error Occurred - Content Not Present')
            temp_course = copy.deepcopy(course)
            temp_course.pop('_id', 'qwe')
            temp_course['error'] = 'content'
            db_operation_status = CourseAlt.upsert_courses([temp_course])
            if not db_operation_status:
                print('UNABLE to Mark in DB')
            return

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
    # except:
    #     print('An Error Occurred')
    #     print('Course:', course_url)
