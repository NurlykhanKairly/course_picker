from django.urls import path

from . import views

urlpatterns = [
    path('course_suggest/', views.CourseSuggest.as_view()),
]