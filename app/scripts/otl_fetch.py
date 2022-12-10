import requests

from course.models import Class, Course
from department.models import Department


def run():
    params = {
        'year': 2022,
        'semester': 3,
        'type': 'ALL',
        'department': 'HSS',
        'level': 'ALL',
        'order': 'class_no',
        'limit': 300,
    }
    response = requests.get("https://otl.kaist.ac.kr/api/lectures", params=params).json()
    for lecture in response:
        course = Course.objects.filter(title=lecture['old_code'])
        if course.exists():
            course = course.first()
        else:
            department = Department.objects.filter(code=lecture['department_code']).first()
            course_type = 3 if lecture['type_en'] == 'Major Elective' else 2
            course = Course(
                title=lecture['old_code'],
                department=department,
                type=course_type,
                credit=lecture['credit'],
            )
            course.save()

        lecture_model = Class(
            title=lecture['title_en'],
            course=course,
            grade=lecture['grade'],
            load=lecture['load'],
            speech=lecture['speech'],
            class_times=lecture['classtimes']
        )
        lecture_model.save()
        print(lecture['old_code'], lecture['grade'], lecture['load'], lecture['speech'])

