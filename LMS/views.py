from LMS.models import *
from LMS.forms import *
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from _datetime import date
from django.db import IntegrityError
from .decorators import unauthenticated_user
from .decorators import allowed_users
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render



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

@unauthenticated_user
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            
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

@unauthenticated_user
def user_login(request):
    context = {"login_errors": []}

    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        context["form"] = form

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                context["login_errors"].append("Invalid login details supplied.")
        else:
            print(form.errors)
            context["login_errors"] = (form.errors)

    form = LoginForm()
    context["form"] = form
    return render(request = request, template_name = "login.html", context=context)

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
     
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            data = search_form.cleaned_data['search']
            option = search_form.cleaned_data['options']
            if option == "1":
                results = ISBN.objects.filter(genre__icontains=data)

                page = request.GET.get('page')
                paginator = Paginator(results, 10)
                try:
                    results = paginator.page(page)
                except PageNotAnInteger:
                    results = paginator.page(1)
                except EmptyPage:
                    results = paginator.page(paginator.num_pages)

            elif option == "2":
                results = ISBN.objects.filter(title__icontains=data)

                page = request.GET.get('page')
                paginator = Paginator(user_list, 10)
                try:
                    results = paginator.page(page)
                except PageNotAnInteger:
                    results = paginator.page(1)
                except EmptyPage:
                    results = paginator.page(paginator.num_pages)

            elif option == "3":
                results = ISBN.objects.filter(author__icontains=data)
                page = request.GET.get('page')
                paginator = Paginator(results, 10)
                try:
                    results = paginator.page(page)
                except PageNotAnInteger:
                    results = paginator.page(1)
                except EmptyPage:
                    results = paginator.page(paginator.num_pages)

            elif option == "4":
                results = ISBN.objects.filter(ISBN__icontains=data)

                page = request.GET.get('page')
                paginator = Paginator(results, 10)
                try:
                    results = paginator.page(page)
                except PageNotAnInteger:
                    results = paginator.page(1)
                except EmptyPage:
                    results = paginator.page(paginator.num_pages)

                return render(request, 'search.html', {'search_form': search_form, 'results': results})
    else:
        results = []
        search_form = SearchForm()
    
    return render(request, 'search.html', context = {'search_form': search_form, 'results': results})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password successfully updated.')
            return redirect(reverse('home'))
        else:
            messages.error(request, 'Please correct errors.')
    else:
        form = PasswordChangeForm(request.user)
        for field in form.fields:
            form.fields[field].widget.attrs.update({'class' : 'form-control'})
    return render(request, 'change_password.html', {'form': form})

@login_required
@allowed_users(allowed_roles=['admin','staff'])
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            try:
                form.save(commit=True)
                messages.success(request, 'Category successfully added.')
                return redirect('/LMS/staff_page')
            except IntegrityError:
                form.save(commit=False)
                messages.error(request, 'Category already exists.')
                return redirect('/LMS/staff_page')
    
    return render(request, 'add_category.html', {'form': form})

@login_required
@allowed_users(allowed_roles=['admin','staff'])
def add_book(request):
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST)
        if ISBN.objects.get(ISBN=form['ISBN'].value()) == None:
            if form.is_valid():
                form.save(commit=True)
        book = Book(isbn=ISBN.objects.get(ISBN=form['ISBN'].value()), location=form['location'].value())
        book.save()
        messages.success(request, 'Book successfully added.')
        return redirect('/LMS/staff_page')
            
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

@login_required
@allowed_users(allowed_roles=['admin','staff'])
def add_staff(request):
    if request.method == 'POST':
        staff_form = StaffForm(request.POST)
        profile_form = StaffProfileForm(request.POST)

        if staff_form.is_valid() and profile_form.is_valid():
            staff = staff_form.save()

            staff.set_password(staff.password)
            staff.save()
            
            group = Group.objects.get(name='staff')
            staff.groups.add(group)
            
            profile = profile_form.save(commit=False)
            profile.user = staff
            
            profile.save()
            messages.success(request, 'Staff successfully added.')
            return redirect('/LMS/staff_page')
    else:
        staff_form = StaffForm()
        profile_form = StaffProfileForm()
    return render(request, 'add_staff.html', context = {'staff_form': staff_form, 'profile_form': profile_form})

@login_required
@allowed_users(allowed_roles=['admin','customer'])
def returns(request):
    context_dict = {}
    try:
        books = Book.objects.filter(taken_out=Member.objects.get(user=request.user))
        times_left = []
        for book in books:
            time = (book.loan_until - date.today()).days
            if time < 0:
                new_time = "Overdue by: " + str(time)
                times_left.append(new_time)
            else:
                times_left.append(time)
        if books:
            context_dict['books'] = zip(books, times_left)
        else:
            context_dict['books'] = None
    except:
        context_dict['books'] = None
    
    if request.method == 'POST':
        book = None
        for key in request.POST.keys():
            if key.startswith('return:'):
                book = key[7:]
                break
        if book:
            book = Book.objects.get(pk_num=book)
            book.taken_out = None
            book.save()
            context_dict['returned'] = book.location
        return redirect('/LMS/returns')
    return render(request, 'returns.html', context=context_dict)

@login_required
@allowed_users(allowed_roles=['admin','staff'])
def staff_page(request):
    return render(request, 'staff_page.html')

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        books = ISBN.objects.filter(category=category)
        context_dict['books'] = books
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['books'] = None
    return render(request, 'category.html', context=context_dict)

def show_isbn(request, isbn):
    context_dict = {}
    try:
        isbn = ISBN.objects.get(ISBN=isbn)
        context_dict['isbn'] = isbn
        books = Book.objects.filter(isbn=isbn)
        context_dict['books'] = books
    except:
        context_dict['isbn'] = None
        context_dict['books'] = None
        
    if request.method == 'POST':
        book = None
        for key in request.POST.keys():
            if key.startswith('loan:'):
                book = key[5:]
                break
        if book:
            user = Member.objects.get(user=request.user)
            amount = Book.objects.filter(taken_out=Member.objects.get(user=request.user)).count()
            if amount < user.book_limit:
                book = Book.objects.get(pk_num=book)
                book.taken_out = user
                book.save()
            else:
                context_dict['limit'] = True
    return render(request, 'isbn.html', context=context_dict)

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Successfully Logged Out.')
    return redirect(reverse('home'))