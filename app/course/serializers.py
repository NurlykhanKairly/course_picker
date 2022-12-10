from .models import Course, Class, CourseHistory

from rest_framework import serializers
from .models import Course, Class


class CourseSerializer(serializers.Serializer):
    class Meta:
        model = Course
        fields = (
            'uuid',
            'title',
            'department',
            'credit',
            'type',
        )


class ClassSerializer(serializers.Serializer):
    class Meta:
        model = Class
        fields = (
            'uuid',
            'title',
            'course',
            'grade',
            'load',
            'speech',
            'class_times',
        )
