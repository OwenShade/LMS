from django.contrib.auth.models import User
from django import forms
from LMS.models import Member, Category, Book, Staff, Library

#Form for adding a category
class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
        help_text="Please enter the new category.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
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
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Book
        fields = ('title', 'category', 'author', 'genre',)

#form for adding a staff member
class StaffForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(max_length=128,
        help_text="Please enter the name of the staff member.")
    
    class Meta:
        model = User
        fields = ('username','password', 'email')
        
class StaffProfileForm(forms.ModelForm):
    role = forms.CharField(max_length=128,
        help_text="Please enter their role.")
    phone = forms.CharField(max_length=128,
        help_text="Please enter their phone number.")
    class Meta:
        model = Staff
        fields = ('role', 'phone', 'reg_library')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(max_length=128,
        help_text="Please enter your name")
    
    class Meta:
        model = User
        fields = ('password', 'username', 'email')
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('reg_library',)
