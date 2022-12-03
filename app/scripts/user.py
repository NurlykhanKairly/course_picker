from student.models import Student
from department.models import Department


def run():
    # Make my student model
    if(Student.objects.filter(student_id='20200846').count() == 0):
        user = Student(
            name = 'Akhdan',
            student_id = '20200846',
            email = 'adzakymaulana15@gmail.com',
            username = '##################',
            password = '##################',
        )
        user.save()
    else:
        user = Student.objects.filter(student_id='20200846').first()
    
    # Make CS, EE, and Others department
    if(Department.objects.filter(code='CS').count() == 0):
        dept_cs = Department(
            id = 0,
            code = 'CS',
            name = 'Gates of Hell',
        )
        dept_cs.save()
    else:
        dept_cs = Department.objects.filter(code='CS').first()

    if(Department.objects.filter(code='EE').count() == 0):
        dept_ee = Department(
        id = 1,
        code = 'EE',
        name = 'Almost Hell',
        )
        dept_ee.save()
    else:
        dept_ee = Department.objects.filter(code='EE').first()

    if(Department.objects.filter(code='HSS').count() == 0):
        dept_ot = Department(
        id = 2,
        code = 'HSS',
        name = 'Hell Itself',
        )
        dept_ot.save()
    else:
        dept_ot = Department.objects.filter(code='HSS').first()
    
    user.major = dept_cs
    user.second_major = dept_ee
    user.save()

    # Add CS, EE, and Others department requirement
    # Ok I think it is not important for now

    return