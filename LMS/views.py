from django.shortcuts import render
from django.http import HttpResponse
from LMS.forms import CategoryForm, BookForm, StaffForm
from django.shortcuts import redirect

#All these views just link back to the home page, still need to link them back to each other
def home(request):
    return render(request, 'home.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def browse(request):
    return render(request, 'browse.html')

def search(request):
    return render(request, 'search.html')

def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return redirect('/LMS/')
        else:
            print(form.errors)
    
    return render(request, 'add_category.html', {'form': form})

def add_book(request):
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return redirect('/LMS/')
        else:
            print(form.errors)
    
    return render(request, 'add_book.html', {'form': form})

def add_staff(request):
    form = StaffForm()

    if request.method == 'POST':
        form = StaffForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return redirect('/LMS/')
        else:
            print(form.errors)
    
    return render(request, 'add_staff.html', {'form': form})



    
