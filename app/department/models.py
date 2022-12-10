import uuid
from django.db import models
# Create your models here.


class Department(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    id = models.IntegerField()
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.code + ' | ' + self.name



class DepartmentRequirements(models.Model):
    DEPARTMENT_TYPES = (
        (0, "Major"),
        (1, "Second Major"),
        (2, "Minor")
    )

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    department = models.ForeignKey(
        'Department',
        on_delete=models.CASCADE,
    )
    credit = models.IntegerField()
    major_mandatory = models.IntegerField()
    elective_major = models.IntegerField()
    type = models.IntegerField(
        choices=DEPARTMENT_TYPES,
        default=0
    )
