from django.contrib import admin

# Register your models here.
from .models import Department, DepartmentRequirements

admin.site.register([
    Department,
    DepartmentRequirements
])
