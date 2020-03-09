from django.shortcuts import render
from django.http import HttpResponse
#from LMS.forms import UserForm, UserProfileForm

#All these views just link back to the home page, still need to link them back to each other
def home(request):
    return render(request, 'LMS/home.html')

def register(request):
    return render(request, 'LMS/register.html')

def login(request):
    return render(request, 'LMS/login.html')

def browse(request):
    return render(request, 'LMS/browse.html')

def search(request):
    return render(request, 'LMS/search.html')

    
