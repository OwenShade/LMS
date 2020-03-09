from django.urls import path
from LMS import views

app_name = 'LMS'

urlpatterns = [
    path('', views.home, name ='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('browse/', views.browse, name='browse' ),
    path('search/', views.search, name='search')
]