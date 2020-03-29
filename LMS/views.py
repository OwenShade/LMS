from django.shortcuts import render
from django.http import HttpResponse
from LMS.models import Library, Member, Staff, Category, ISBN, Book
from LMS.forms import CategoryForm, BookForm, StaffForm, UserForm, UserProfileForm, StaffProfileForm
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def home(request):
    context_dict = {}
    try:
        category_list = Category.objects.order_by('-views')[:5]
        context_dict['categories'] = category_list
    except Category.DoesNotExist:
        context_dict['categories'] = None

    try:
        book_list = ISBN.objects.order_by('-views')[:5]
        context_dict['books'] = book_list
    except ISBN.DoesNotExist:
        context_dict['books'] = None
        
    response = render(request, 'home.html', context=context_dict)
    return response

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'register.html', context ={'user_form': user_form,'profile_form' : profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('home'))
            else:
                return HttpResponse("Your library account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'login.html')

def browse(request):
    context_dict = {}
    try:
        category_list = Category.objects.all()
        context_dict['categories'] = category_list
    except Category.DoesNotExist:
        context_dict['categories'] = None
    response = render(request, 'browse.html', context=context_dict)
    return response

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
            book = Book(isbn=ISBN.objects.get(ISBN=form['ISBN'].value()), location=Library.objects.get(pk_num=1))
            book.save()
            return redirect('/LMS/')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

def add_staff(request):
    form = StaffForm()

    if request.method == 'POST':
        staff_form = StaffForm(request.POST)
        profile_form = StaffProfileForm(request.POST)

        if staff_form.is_valid() and profile_form.is_valid():
            staff = staff_form.save()

            staff.set_password(staff.password)
            staff.save()
            
            profile = profile_form.save(commit=False)
            profile.user = staff
            
            profile.save()
            
            return redirect('/LMS/')
    else:
        staff_form = StaffForm()
        profile_form = StaffProfileForm()
    return render(request, 'add_staff.html', context = {'staff_form': staff_form, 'profile_form': profile_form})

def returns(request):
    return render(request, 'returns.html')

def staff_page(request):
    return render(request, 'staff_page.html')

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
    return render(request, 'browse.html', context=context_dict)

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('home'))


    
