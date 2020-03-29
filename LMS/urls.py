from django.urls import path
from django.conf.urls import url
from LMS import views

app_name = 'LMS'

urlpatterns = [
    path('', views.home, name ='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('browse/', views.browse, name='browse' ),
    path('search/', views.search, name='search'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_book/', views.add_book, name='add_book'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('returns/', views.returns, name='returns'),
    path('staff_page/', views.staff_page, name='staff_page'),
    path('logout/', views.user_logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('category/<slug:Category_name_slug>/', views.show_category, name='show_category'),
]