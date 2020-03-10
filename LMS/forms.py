from django.contrib.auth.models import User
from django import forms
from LMS.models import Member, Category, Book, Staff 

#Form for adding a category
class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
        help_text="Please enter the new category.")
    
    class Meta:
        model = Category
        fields = ('name',)

#form for adding a book
class BookForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
        help_text="Please enter the book title.")
    category = forms.CharField(max_length=128,
        help_text="Please enter the Category.")
    author = forms.CharField(max_length=128,
        help_text="Please enter the author of the book.")
    genre = forms.CharField(max_length=128,
        help_text="Please enter the genre.")

    class Meta:
        model = Book
        fields = ('title', 'category', 'author', 'genre',)

#form for adding a staff member
class StaffForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
        help_text="Please enter the name of the staff member.")
    role = forms.CharField(max_length=128,
        help_text="Please enter their role.")
    phone = forms.CharField(max_length=128,
        help_text="Please enter their phone number.")
    
    class Meta:
        model = Staff
        fields = ('name', 'role', 'phone',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    name = forms.CharField(max_length=128,
        help_text="Please enter your full name.")
    email = forms.CharField(max_length=128,
        help_text="Please enter your email.")

    class Meta:
        model = Member
        fields = ('name', 'email')