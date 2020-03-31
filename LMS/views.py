from LMS.models import *
from LMS.forms import *
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from _datetime import date, timedelta
from django.db import IntegrityError
from .decorators import unauthenticated_user
from .decorators import allowed_users
from django.contrib.auth.models import Group

#Simple view that is mapped to the base html so that we can check what level of
#permissions a user has on all pages of the site, in order to decide what type of content they are shown
def if_staff(request):
    if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group in ["admin", "staff"]:
                    return True
                else:
                    return False

#View to map to the home page that filters through to find the most popular categories and books 
def home(request):
    context_dict = {}
    context_dict['staff'] = if_staff(request)
    try:
        #finds the 5 most popular categories by check their amount of views and appends them to the context dict
        category_list = Category.objects.order_by('-views')[:5]
        context_dict['categories'] = category_list
    except Category.DoesNotExist:
        context_dict['categories'] = None

    try:
        #finds the 5 most popular books by check their amount of views and appends them to the context dict
        book_list = ISBN.objects.order_by('-views')[:5]
        context_dict['books'] = book_list
    except ISBN.DoesNotExist:
        context_dict['books'] = None
    
    #returns the request to the home page along with the context dictionary
    response = render(request, 'home.html', context=context_dict)
    return response

#Uses decorators to make sure only unauthenticated user can access the register page
@unauthenticated_user
def register(request):
    registered = False

    if request.method == 'POST':
        #display the forms to the user on the html page
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        #If the details entered in the forms are valide, create the new user instance using the entered values
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            group = Group.objects.get(name='member')
            user.groups.add(group)
            
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            
            profile.save()

            registered = True
        #if the details entered aren't appropriate, print the errors.
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'register.html', context ={'user_form': user_form,'profile_form' : profile_form, 'registered': registered})

#Uses decorators to make sure only unauthenticated user can access the login page
@unauthenticated_user
def user_login(request):
    context = {"login_errors": []}

    if request.method == 'POST':
        #diplay the login form to the user through the html page
        form = LoginForm(request=request, data=request.POST)
        context["form"] = form
        #if the values entered are appriopriate, validate that the username and password are correct and link up to an account
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                #if the login is correct, login the user and display a success message
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return HttpResponseRedirect(request.session['login_from'])
            else:
                #if the login is wrong, tell the user
                context["login_errors"].append("Invalid login details supplied.")
        else:
            print(form.errors)
            context["login_errors"] = (form.errors)

    form = LoginForm()
    context["form"] = form
    request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    return render(request = request, template_name = "login.html", context=context)

#view for the brwse page
def browse(request):
    context_dict = {}
    #adds a boolean to the context dict describing whether or not a user is a staff member
    #(only customers should be able to access the browse page)
    context_dict['staff'] = if_staff(request)
    try:
        #includes all the category names in the category list then appends this to the context dictionary to be send to browse.html
        category_list = Category.objects.all()
        context_dict['categories'] = category_list
    except Category.DoesNotExist:
        context_dict['categories'] = None
    response = render(request, 'browse.html', context=context_dict)
    return response

#view for the search page
def search(request):
    context_dict = {}
    context_dict['staff'] = if_staff(request)
    #sends a request to display the search form
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            data = search_form.cleaned_data['search']
            option = search_form.cleaned_data['options']
            #if the user selects genre from the drop down menu, search genres for the data entered at the search bar
            if option == "1":
                results = ISBN.objects.filter(genre__icontains=data)
            #if the user selects title from the drop down menu, search titles for the data entered at the search bar
            elif option == "2":
                results = ISBN.objects.filter(title__icontains=data)
            #if the user selects authors from the drop down menu, search authors for the data entered at the search bar
            elif option == "3":
                results = ISBN.objects.filter(author__icontains=data)
            #if the user selects ISBN from the drop down menu, search ISBN for the data entered at the search bar
            elif option == "4":
                results = ISBN.objects.filter(ISBN__icontains=data)
    else:
        results = []
        search_form = SearchForm()
    context_dict['results'] = results
    context_dict['search_form'] = search_form
    return render(request, 'search.html', context = context_dict)

#Uses decorators to make sure only logged in users can change their password
@login_required
def change_password(request):
    context_dict = {}
    #adds a boolean to the context dict describing whether or not a user is a staff member
    context_dict['staff'] = if_staff(request)
    if request.method == 'POST':
        #display the form to the user
        form = PasswordChangeForm(request.user, request.POST)
        #if the form is correct, update password and display success message, otherwise, ask user to correct errors
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
    context_dict['form'] = form
    return render(request, 'change_password.html', context = context_dict)

#Uses decorators to make sure only logged in staff memebers and admins can add categories
@login_required
@allowed_users(allowed_roles=['admin','staff'])
def add_category(request):
    context_dict = {}
    #adds a boolean to the context dict describing whether or not a user is a staff member
    context_dict['staff'] = if_staff(request)
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        #if the form is correct, let the user know through a redirect message
        if form.is_valid():
            try:
                form.save(commit=True)
                messages.success(request, 'Category successfully added.')
                return redirect('/LMS/staff_page')
            #if the category already exists, let the user know through a redirect message
            except IntegrityError:
                form.save(commit=False)
                messages.error(request, 'Category already exists.')
                return redirect('/LMS/staff_page')
    context_dict['form'] = form
    return render(request, 'add_category.html', context = context_dict)

#Uses decorators to make sure only logged in staff memebers and admins can add books
@login_required
@allowed_users(allowed_roles=['admin','staff'])
def add_book(request):
    context_dict = {}
    #adds a boolean to the context dict describing whether or not a user is a staff member
    context_dict['staff'] = if_staff(request)
    isbn_form = ISBNForm()
    book_form = BookForm()
    #display the appropriate form depending on the request
    if request.method == 'POST':
        if 'submit_isbn' in request.POST:
            #display the form which allows staff to add a new book
            #if successfull, tell the user with a redirect message
            form = ISBNForm(request.POST)
            if form.is_valid():
                form.save(commit=True)
                book = Book(isbn=ISBN.objects.get(ISBN=form['ISBN'].value()), location=form['location'].value())
                book.save()
                messages.success(request, 'Book successfully added.')
        elif 'submit_book' in request.POST:
            #display the form which allows staff to add copies of the same book
            #if successfull, tell the user with a redirect message
            form = BookForm(request.POST)
            if form.is_valid():
                isbn = ISBN.objects.filter(ISBN=form['ISBN'].value())
                if isbn.count() != 0:
                    book = Book(isbn=isbn[0], location = form['location'].value())
                    book.save()
                    messages.success(request, 'Copy of book successfully added.')
                else:
                    form.add_error('ISBN', 'No ISBN Found')
        return redirect('/LMS/staff_page')
            
    else:
        isbn_form = ISBNForm()
        book_form = BookForm()
    context_dict['isbn_form'] = isbn_form
    context_dict['book_form'] = book_form
    return render(request, 'add_book.html', context = context_dict)

#Uses decorators to make sure only logged in staff memebers and admins can add new staff members
@login_required
@allowed_users(allowed_roles=['admin','staff'])
def add_staff(request):
    context_dict = {}
    #adds a boolean to the context dict describing whether or not a user is a staff member
    context_dict['staff'] = if_staff(request)
    #Shows the staff form and profile form to the user when called upon
    #sets the new staffs attributes according to the data added and assigns the staff member to the staff group
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
            #sends a message when redirected to let the user know they have been successfully added the record
            messages.success(request, 'Staff successfully added.')
            return redirect('/LMS/staff_page')
    else:
        staff_form = StaffForm()
        profile_form = StaffProfileForm()
    context_dict['staff_form'] = staff_form
    context_dict['profile_form'] = profile_form
    return render(request, 'add_staff.html', context = context_dict)

#Uses decorators to make sure only logged in members (users) can return books
@login_required
@allowed_users(allowed_roles=['member'])
def returns(request):
    context_dict = {}
    #adds a boolean to the context dict describing whether or not a user is a staff member
    context_dict['staff'] = if_staff(request)
    try:
        books = Book.objects.filter(taken_out=Member.objects.get(user=request.user))
        times_left = []
        for book in books:
            if book.loan_until != None:
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
                book = Book.objects.get(pk_num=book)
                book.taken_out = None
                book.loan_until = None
                book.save()
                break
        return redirect('/LMS/returns')
    return render(request, 'returns.html', context=context_dict)

#Uses decorators to make sure only logged in staff members and admins can access the staff page
@login_required
@allowed_users(allowed_roles=['admin','staff'])
def staff_page(request):
    context_dict = {}
    #adds a boolean to the context dict describing whether or not a user is a staff member
    context_dict['staff'] = if_staff(request)
    try:
        books = Book.objects.filter(back_in=False, taken_out=None)
        context_dict['books'] = books
    except:
        context_dict['books'] = None
    
    if request.method == 'POST':
        
        #Returns book to location
        for key in request.POST.keys():
            if key.startswith('back_in:'):
                book = key[8:]
                location = request.POST['location']
                book = Book.objects.get(pk_num=book)
                book.back_in = True
                book.location = location
                book.save()
                break
            
        return redirect('/LMS/staff_page')
    return render(request, 'staff_page.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    #adds a boolean to the context dict describing whether or not a user is a staff member
    context_dict['staff'] = if_staff(request)
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
    #adds a boolean to the context dict describing whether or not a user is a staff member
    context_dict['staff'] = if_staff(request)
    try:
        isbn = ISBN.objects.get(ISBN=isbn)
        context_dict['isbn'] = isbn
        books = Book.objects.filter(isbn=isbn)
        context_dict['books'] = books
        if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group in ["admin", "staff"]:
                    context_dict['staff'] = True
    except:
        context_dict['isbn'] = None
        context_dict['books'] = None
        context_dict['staff'] = False
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
                context_dict['user'] = user
                book.save()
                return redirect('/LMS/'+str(isbn.ISBN))
            else:
                context_dict['limit'] = True
    return render(request, 'isbn.html', context=context_dict)

#Uses decorators to make sure only logged in users can log out
@login_required
def user_logout(request):
    logout(request)
    #sends a message when redirected to let the user know they have been successfully logged out
    messages.success(request, 'Successfully Logged Out.')
    return redirect(reverse('home'))

#Uses decorators to make sure only logged in staff members and admins can extend loans
@allowed_users(allowed_roles=['admin','staff'])
def extend_loan(request):
    context_dict = {}
    #adds a boolean to the context dict describing whether or not a user is a staff member
    context_dict['staff'] = if_staff(request)
    try:
        books = Book.objects.exclude(taken_out=None)
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
            if key.startswith('extend:'):
                book = key[7:]
                book = Book.objects.get(pk_num=book)
                book.loan_until = book.loan_until + timedelta(days=7)
                book.save()
                break
        return redirect('/LMS/extend_loan')
    return render(request, 'extend_loan.html', context=context_dict)