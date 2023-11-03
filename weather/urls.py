# here we are import path from in-built django-urls
from django.urls import path

# here we are importing all the Views from the views.py file
from .views import * 


urlpatterns = [
    path('',weather, name='weather'),
    path('encode/',encode_chunk,name='encode'),
    path('decode/',decode_chunk,name='decode'),
    path('control_timer/', control_timer, name='control_timer'),
]
