from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from pprint import pprint

# client = MongoClient('mongodb://forum_analyzer:admin123@ds157901.mlab.com:57901/moocrecv2')
client = MongoClient('mongodb://localhost:27017/moocrecv2')

database = client.moocrecv2


class Thread:

    @staticmethod
    def save_threads(threads):
        try:
            result = database.threads.insert(threads)
            return result
        except ServerSelectionTimeoutError:
            print('Error Connecting to Database')
        except:
            print('An Error Occurred')

    @staticmethod
    def upsert_threads(threads):
        try:
            for thread in threads:
                database.threads.update_one({'id': thread['id']}, {"$set": thread}, upsert=True)
            return True
        except ServerSelectionTimeoutError:
            print('Error Connecting to Database')
            return False
        except:
            print('An Error Occurred')
            return False

    @staticmethod
    def get_discussion_threads_with_responses(course_id):
        try:
            results = database.threads.find(
                {
                    'course_id': course_id,
                    'thread_type': 'discussion',
                    '$or': [
                        {'children': {'$exists': 'true'}},
                        {'non_endorsed_responses': {'$exists': 'true'}}
                    ]
                }
            ).limit(100)
            return results
        except ServerSelectionTimeoutError:
            print('Error Connecting to Database')
            return

    @staticmethod
    def get_sentiment_analyzed_threads():
        try:
            results = database.Threads.find({
                'course_id': 'course-v1:UCSanDiegoX+DSE200x+1T2019a',
                'thread_type': 'discussion',
                '$or': [
                    {'children': {'$exists': 'true'}},
                    {'non_endorsed_responses': {'$exists': 'true'}}
                ],
                '$and': [{'is_sentiment_analyzed': {'$exists': 'true'}}, {'sentiment_score': {'$exists': 'true'}}]
            }, {'is_sentiment_analyzed': 1, 'sentiment_score': 1}).sort({'sentiment_score': -1})
            return results
        except:
            return []


class Course:

    @staticmethod
    def upsert_courses(courses):
        try:
            for course in courses:
                try:
                    database.courses.update_one({'key': course['key']}, {"$set": course}, upsert=True)
                except KeyError:
                    database.courses.update_one({'_id': course['_id']}, {"$set": course}, upsert=True)
            return True
        except ServerSelectionTimeoutError:
            print('Error Connecting to Database')
            return False
        except:
            print('An Error Occurred')
            return False

    @staticmethod
    def upsert_courses_alt(courses):
        try:
            for course in courses:
                if 'id' not in course.keys():
                    database.courses.insert_one(course)
                else:
                    database.courses.update_one({'_id': course['_id']}, {"$set": course}, upsert=True)
            return True
        except ServerSelectionTimeoutError:
            print('Error Connecting to Database')
            return False
        except:
            print('An Error Occurred')
            return False

    @staticmethod
    def get_course(course_key):
        try:
            courses = database.courses.find({'key': course_key})
            return courses[0]
        except:
            return None
            pass

    @staticmethod
    def get_courses():
        try:
            courses = database.courses.find()
            return courses
        except:
            return None
            pass


class Subject:

    @staticmethod
    def upsert_subjects(subjects):
        try:
            for subject in subjects:
                database.subjects.update_one({'key': subject['uuid']}, {"$set": subject}, upsert=True)
            return True
        except ServerSelectionTimeoutError:
            print('Error Connecting to Database')
            return False
        except:
            print('An Error Occurred')
            return False


def convert_platform_representation_to_string():
    courses = Course.get_courses()
    new_courses = []
    for temp_course in courses:
        course = temp_course
        try:
            if course['platform'] == 0:
                course['platform'] = 'Edx'
            elif course['platform'] == 1:
                course['platform'] = 'FutureLearn'
            # else:
            # print('The attribute \'platform\' does not exist')
            # course['platform'] = 'Edx'
        except KeyError:
            course['platform'] = 'Edx'
        new_courses.append(course)

    result = Course.upsert_courses(new_courses)
    print('Result =', result)


convert_platform_representation_to_string()
