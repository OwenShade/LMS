from django.shortcuts import render
from django.http import HttpResponse
from LMS.forms import CategoryForm, BookForm, StaffForm, UserForm
from django.shortcuts import redirect
from django.views.generic import ListView

def home(request):
    return render(request, 'home.html')

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'register.html', context ={'user-form': user_form, 'registered': registered})

def login(request):
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

    
