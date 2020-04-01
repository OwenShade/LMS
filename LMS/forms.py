from django.contrib.auth.models import User
from django import forms
from LMS.models import Member, Category, Book, Staff, ISBN
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm, UserCreationForm

#Form for adding a category
#categories only have two fields. One is shown on the form (name) and the other, views, is initialised to zero when the new category is made
class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
        help_text="Please enter the new category.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    #script for styling the form
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control m-1'})

    class Meta:
        model = Category
        fields = ('name',)

#form for adding a book
#display input options to the user so that they can enter the ISBN, title, author, category, genre, and shelf location.
class ISBNForm(forms.ModelForm):
    ISBN = forms.IntegerField(min_value=1000000000, max_value=9999999999, help_text="Please enter the ISBN.", label="ISBN")
    title = forms.CharField(max_length=128, help_text="Please enter the book title.")
    category = forms.ModelChoiceField(Category.objects.all(), help_text="Please select a category.")
    author = forms.CharField(max_length=128, help_text="Please enter the author of the book.")
    genre = forms.CharField(max_length=128, help_text="Please enter the genre.")
    location = forms.CharField(max_length=16, help_text="Please enter the shelf that this book is on.")

    #script for styling the form
    def __init__(self, *args, **kwargs):
        super(ISBNForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

    class Meta:
        model = ISBN
        fields = ('ISBN', 'title', 'category', 'author', 'genre',)

class StaffForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    role = forms.CharField(max_length=128)
    phone = forms.IntegerField()

    #script for styling the form
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role', 'phone' )

#first form for adding a staff member
class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    
    #script for styling the form
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

#allows the user to login, by asking for the users credentials: username and password
class LoginForm(AuthenticationForm):
    username = forms.CharField(help_text="Username")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Password")

    class Meta:
        model = Member
        fields = ('username', 'password')
        
#form allowing a staff member to create a copy of a book with a different location if needed
class BookForm(forms.Form):
    ISBN = forms.IntegerField(min_value=1000000000, max_value=9999999999, help_text="Please enter the ISBN.", label="ISBN")
    location = forms.CharField(max_length=16, help_text="Please enter the shelf that this book is on.")