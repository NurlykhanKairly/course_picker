from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, F, Value
from django.core import serializers as ser

from course.serializers import ClassSerializer

from department.models import Department
from course.models import Course, Class, CourseHistory
from student.models import Student



class CourseSuggestSerializer(serializers.Serializer):
    credits = serializers.IntegerField()
    humanities = serializers.IntegerField()
    first_major_required = serializers.IntegerField()
    first_major_elective = serializers.IntegerField()
    second_major_required = serializers.IntegerField()
    second_major_elective = serializers.IntegerField()

# Create your views here.

def intersect(class_times1, class_times2):
    for time1 in class_times1:
        for time2 in class_times2:
            if time1['day'] == time2['day']:
                if min(time1['end'], time2['end']) >= max(time1['begin'], time2['begin']):
                    return True
    return False


def get_best_option(greedy, classes):
    student = Student.objects.filter(username='nurlykhan').first()
    student_history = CourseHistory.objects.filter(student=student).first()

    for cl in classes:
        if cl.course in student_history.courses.all() or cl.course.credit < 3:
            continue
        intersect_any = False
        for cl2 in greedy:
            if intersect(cl.class_times, cl2.class_times):
                intersect_any = True
                break
        if not intersect_any:
            return cl


class CourseSuggest(APIView):
    def get(self, request):
        return Response(data='Hello World!', status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CourseSuggestSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            credits = serializer.data.get('credits')
            humanities = serializer.data.get('humanities')
            first_major_required = serializer.data.get('first_major_required')
            first_major_elective = serializer.data.get('first_major_elective')
            second_major_required = serializer.data.get('second_major_required')
            second_major_elective = serializer.data.get('second_major_elective')
            student = Student.objects.filter(username='nurlykhan').first()

            greedy_taking = []
            courses = []
            while True:
                at_least_one_taken = False
                major = student.major
                second_major = student.second_major
                classes = None
                if first_major_required > 0:
                    classes = Class.objects.filter(course__department=major, course__type=2).annotate(
                        overall_rating=(F('grade') + F('load') + F('speech')) / 3).all().order_by('-overall_rating').all()

                    best_option = get_best_option(greedy_taking, classes)
                    if best_option:
                        first_major_required -= 1
                        greedy_taking.append(best_option)
                        at_least_one_taken = True

                if first_major_elective > 0:
                    classes = Class.objects.filter(course__department=major, course__type=3).annotate(
                        overall_rating=(F('grade') + F('load') + F('speech')) / 3).all().order_by(
                        '-overall_rating').all()
                    best_option = get_best_option(greedy_taking, classes)
                    if best_option:
                        first_major_elective -= 1
                        greedy_taking.append(best_option)
                        at_least_one_taken = True

                if second_major_required > 0:
                    classes = Class.objects.filter(course__department=second_major, course__type=2).annotate(
                        overall_rating=(F('grade') + F('load') + F('speech')) / 3).all().order_by(
                        '-overall_rating').all()
                    best_option = get_best_option(greedy_taking, classes)
                    if best_option:
                        second_major_required -= 1
                        greedy_taking.append(best_option)
                        at_least_one_taken = True

                if second_major_elective > 0:
                    classes = Class.objects.filter(course__department=second_major, course__type=2).annotate(
                        overall_rating=(F('grade') + F('load') + F('speech')) / 3).all().order_by(
                        '-overall_rating').all()
                    best_option = get_best_option(greedy_taking, classes)
                    if best_option:
                        second_major_elective -= 1
                        greedy_taking.append(best_option)
                        at_least_one_taken = True

                if humanities > 0:
                    humanities_department = Department.objects.filter(code='HSS').first()
                    classes = Class.objects.filter(course__department=humanities_department).annotate(
                        overall_rating=(F('grade') + F('load') + F('speech')) / 3).all().order_by(
                        '-overall_rating').all()
                    best_option = get_best_option(greedy_taking, classes)
                    if best_option:
                        humanities -= 1
                        greedy_taking.append(best_option)
                        at_least_one_taken = True

                if not at_least_one_taken:
                    break

            print('----- SUGGESTED_COURSES -----')
            for cl in greedy_taking:
                print(cl.title, '|', cl.course.department, '|', ('Major Elective' if cl.course.type == 3 else 'Major Required'), '| overall_rating = ', (cl.load + cl.grade + cl.speech) / 3, 'load = ', cl.load, 'speech = ', cl.speech, 'grade = ', cl.grade)
                print(cl.class_times)
                print('----------')
            #schedule_ser = ClassSerializer(data=greedy_taking, many=True)
            #if schedule_ser.is_valid():
            uuids_classes = []
            for cl in greedy_taking:
                uuids_classes.append(cl.uuid)
            sr = ClassSerializer(data=Class.objects.filter(pk__in=uuids_classes), many=True)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)
