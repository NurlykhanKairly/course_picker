from django.contrib import admin

# Register your models here.
from .models import Course, Class, CourseHistory

admin.site.register([
    Course,
    Class,
    CourseHistory
])
