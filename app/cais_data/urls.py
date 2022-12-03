from django.urls import path

from . import views

app_name = 'cais_data'
urlpatterns = [
    # ex: /cais_data/
    path('', views.cais_mining, name='cais_mining'),
]