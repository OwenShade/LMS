from django.contrib.auth.models import User
from django import forms
from LMS.models import Member, Category, Book, Staff, ISBN
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm

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
    ISBN = forms.IntegerField(min_value=1000000000, max_value=9999999999, help_text="Please enter the ISBN.", label="ISBN")
    title = forms.CharField(max_length=128, help_text="Please enter the book title.")
    category = forms.ModelChoiceField(Category.objects.all(), help_text="Please select a category.")
    author = forms.CharField(max_length=128, help_text="Please enter the author of the book.")
    genre = forms.CharField(max_length=128, help_text="Please enter the genre.")
    location = forms.CharField(max_length=16, help_text="Please enter the shelf that this book is on.")

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

    class Meta:
        model = ISBN
        fields = ('ISBN', 'title', 'category', 'author', 'genre',)

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
        fields = ('role', 'phone',)

class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=128,
        help_text="Name")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Password")
    email = forms.EmailField(help_text="Email")
    
    class Meta:
        model = User
        fields = ('password', 'username', 'email',)
        
class UserProfileForm(UserForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

    class Meta:
        model = Member
        fields = ('username','password', 'email',)
        
class SearchForm(forms.Form):
    search = forms.CharField(max_length=128)
    options = forms.ChoiceField(choices=[("1","Genre"), ("2","Title"), ("3","Author",), ("4","ISBN")], help_text="Choose what to search.")
class LoginForm(AuthenticationForm):
    username = forms.CharField(help_text="Username")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Password")

    class Meta:
        model = Member
        fields = ('username', 'password')
