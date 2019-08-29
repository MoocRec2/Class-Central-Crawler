from subject import retrieve_courses_from_subject

subjects_info_list = [
    {'key': 'ai', 'url': 'https://www.classcentral.com/subject/ai'},
    {'key': 'bl0ck_crypt0', 'url': 'https://www.classcentral.com/subject/blockchain-cryptocurrency'},
]
for subject_info in subjects_info_list:
    retrieve_courses_from_subject(subject_info)
