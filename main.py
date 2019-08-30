from subject import retrieve_courses_from_subject
from thread import retrieve_thread_of_course
from db_connector import Course
from pprint import pprint

subjects_info_list = [
    {'key': 'ai', 'url': 'https://www.classcentral.com/subject/ai'},
    {'key': 'bl0ck_crypt0', 'url': 'https://www.classcentral.com/subject/blockchain-cryptocurrency'},
    {'key': 'stats', 'url': 'https://www.classcentral.com/subject/statistics'},
]
# Retrieve Course of Subject
# for subject_info in subjects_info_list:
#     retrieve_courses_from_subject(subject_info)
#
# courses = list(Course.get_courses({'platform': 'Coursera'}))

# Retrieve Threads of Course
# for course in courses:
#     retrieve_thread_of_course(course)
#     break

retrieve_thread_of_course({'course_link': 'https://www.classcentral.com/course/coursera-machine-learning-835'})
