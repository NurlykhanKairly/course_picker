import uuid

from django.db import models
from department.models import Department
# Create your models here.


class Student(models.Model):
    YEAR_CHOICE = (
        (1, "Freshman"),
        (2, "Sophomore"),
        (3, "Junior"),
        (4, "Senior"),
        (5, "Extension"),
    )

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=150)
    student_id = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    major = models.ForeignKey(
        'department.Department',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Student Major Department',
        related_name='student_main_major',
    )
    second_major = models.ForeignKey(
        'department.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Student Second Major Department',
        related_name = 'student_second_major',
    )
    minor = models.ForeignKey(
        'department.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Student Minor Department',
        related_name='student_minor',
    )
    year = models.IntegerField(
        choices=YEAR_CHOICE,
        default=1
    )

    class Meta:
        verbose_name = 'KAIST Student'
        verbose_name_plural = 'KAIST Students'
