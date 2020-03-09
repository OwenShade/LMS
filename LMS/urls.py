from django.urls import path
from LMS import views

app_name = 'LMS'

urlpatterns = [
    path('home', views.home, name ='home'),
    path('register', views.register, name='register'),
]