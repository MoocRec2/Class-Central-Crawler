from subject import retrieve_courses_from_subject
from thread import retrieve_thread_of_course
from db_connector import Course
from db_connector import CourseAlt
from pprint import pprint

subjects_info_list = [
    {'key': 'ai', 'url': 'https://www.classcentral.com/subject/ai'},
    {'key': 'bl0ck_crypt0', 'url': 'https://www.classcentral.com/subject/blockchain-cryptocurrency'},
    {'key': 'stats', 'url': 'https://www.classcentral.com/subject/statistics'},
]
# Retrieve Course of Subject
# for subject_info in subjects_info_list:
#     print('-------------------------------------------------------------', subject_info['key'])
#     retrieve_courses_from_subject(subject_info)

# courses = list(Course.get_courses({'platform': 'Coursera'}))
courses = list(CourseAlt.get_courses({'description': {'$exists': 0}, 'error': {'$exists': 0}}))
length = courses.__len__()
print('Course Count:', length)

# filtered_courses = []
# for course in courses:
#     if 'description' not in course.keys()

# Retrieve Threads of Course
count = 0
for course in courses:
    count += 1
    retrieve_thread_of_course(course)
    print('Iteration Complete, Overall Progress:', (count / length) * 100, count, 'done,', length - count, 'more to go')
# break

# retrieve_thread_of_course({'course_link': 'https://www.classcentral.com/course/coursera-machine-learning-835'})
