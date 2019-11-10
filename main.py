from subject import retrieve_courses_from_subject
from thread import retrieve_thread_of_course
from db_connector import Course
from db_connector import CourseAlt
from pprint import pprint
import time
from threading import Thread
import numpy

'''
    Process
    
    Subject 1-* Courses 1-* Threads
    
    1 - Retrieve Courses of Subjects
    2 - Retrieve Threads of Courses
'''

start_time = time.time()

subjects_info_list = [
    {'key': 'ai', 'url': 'https://www.classcentral.com/subject/ai'},
    {'key': 'bl0ck_crypt0', 'url': 'https://www.classcentral.com/subject/blockchain-cryptocurrency'},
    {'key': 'stats', 'url': 'https://www.classcentral.com/subject/statistics'},
]

# ----- Retrieve Courses of Subjects -----
print('Phase 1 - Retrieving Courses of Subjects')
for subject_info in subjects_info_list:
    print('Subject:', subject_info['key'])
    retrieve_courses_from_subject(subject_info)

print('Phase 1 - Retrieving Courses of Subjects - Finished')
# The above code will gather the courses and save them in the database
# The below code will get the same data from the database
courses = list(Course.get_courses({'platform': 'Coursera'}))
# courses = list(CourseAlt.get_courses({'description': {'$exists': 0}, 'error': {'$exists': 0}}))
# courses = list(CourseAlt.get_courses({'link_fixed': False}))
length = courses.__len__()
print('Course Count:', length)


# filtered_courses = []
# for course in courses:
#     if 'description' not in course.keys()

# Retrieve Threads of Course
# count = 0
# for course in courses:
#     count += 1
#     retrieve_thread_of_course(course)
#     print('Iteration Complete, Overall Progress:', (count / length) * 100, count, 'done,', length - count, 'more to go')
# break


def wrapper(courses_inner, thread_num):
    # Wrapper method for analyzing a set of Courses
    count = 0
    for course in courses_inner:
        count += 1
        retrieve_thread_of_course(course)
        len = courses_inner.__len__()
        progress = (count / len) * 100
        print('THREAD:', thread_num, 'Progress:', round(progress), '%, COMPLETED:', count, 'REMAINING:', len - count)
        # print('THREAD:', thread_num, 'Iteration Complete, Overall Progress:', (count / courses_inner.__len__()) * 100,
        #       count, 'done,', courses_inner.__len__() - count, 'more to go')

    return


# retrieve_thread_of_course({'course_link': 'https://www.classcentral.com/course/coursera-machine-learning-835'})


# ----- Retrieve Threads of Courses -----
print('Phase 2 - Retrieving Threads from Courses')

''' 
    Splitting the Courses to Multiple Sets
    Reason: So that the Threads can be retrieved in parallel
'''
l = numpy.array_split(numpy.array(courses), 5)
print('Length:', l.__len__())

thread_list = []
thread_num = 0
for course_list in l:
    thread_num += 1
    thread = Thread(target=wrapper, args=(course_list, thread_num))
    thread_list.append(list)
    thread.start()

end_time = time.time()
time_elapsed = end_time - start_time
print('Time Elapsed:', time_elapsed, 'seconds')
