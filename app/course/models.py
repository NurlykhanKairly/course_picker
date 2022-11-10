import uuid

from django.db import models

# Create your models here.


class Course(models.Model):
    COURSE_TYPES = (
        (0, "Basic Required"),
        (1, "Basic Elective"),
        (2, "Major Required"),
        (3, "Major Elective"),
    )

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=50)
    department = models.ForeignKey(
        'department.Department',
        on_delete=models.SET_NULL,
        null=True
    )
    credit = models.IntegerField(default=3)
    type = models.IntegerField(
        choices=COURSE_TYPES,
        default=0
    )


class Class(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=50)
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
    )
    grade = models.IntegerField()
    load = models.IntegerField()
    speech = models.IntegerField()
    class_times = models.JSONField()


class CourseHistory(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    student = models.ForeignKey(
        'student.Student',
        on_delete=models.CASCADE,
    )
    courses = models.ManyToManyField(
        'Course',
    )
