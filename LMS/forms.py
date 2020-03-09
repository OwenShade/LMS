from django.contrib.auth.models import User
from django import forms
from LMS.models import Member, Category, Book

#Form for adding a category
class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
        help_text="Please enter the new category.")
    
    class Meta:
        #Not too sure what is meant to go in here!

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
        #Same here! - Owen.

#form for adding a staff member
class StaffMember(forms.ModelForm):
    name = forms.CharField(max_length=128,
        help_text="Please enter the name of the staff member.")
    role = forms.CharField(max_length=128,
        help_text="Please enter their role.")
    phone = forms.CharField(max_length=128,
        help_text="Please enter their phone number.")
    
    class Meta:
        # same here.

#form for a new user to register themselves
#don't think this works, needs some work
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Member
        fields = ('name', 'email')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('pk_num',) 