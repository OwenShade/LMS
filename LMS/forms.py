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

#first form for adding a staff member
class StaffForm(forms.ModelForm):
    #two fields needed to add a new staff member in the first form.
    #password and username, both are added using text input boxes displayed to the user
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(max_length=128,
        help_text="Please enter the name of the staff member.")
    
    #script for styling the form
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

    class Meta:
        model = User
        fields = ('username','password', 'email')
        
#second form for adding a staff member
class StaffProfileForm(forms.ModelForm):
    #two fields needed to add a new staff member in the second form.
    #role and phone number, both are added using text input boxes displayed to the user
    role = forms.CharField(max_length=128,
        help_text="Please enter their role.")
    phone = forms.CharField(max_length=128,
        help_text="Please enter their phone number.")

    #script for styling the form
    def __init__(self, *args, **kwargs):
        super(StaffProfileForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

    class Meta:
        model = Staff
        fields = ('role', 'phone',)

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

#NOT IN USE
#form for creating a new user, used in the registration page
class UserForm(forms.ModelForm):
    #3 inputs needed for the user to register, all displayed in text boxes. Username, password, and email
    username = forms.CharField(max_length=128,
        help_text="Name")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Password")
    email = forms.EmailField(help_text="Email")
    
    class Meta:
        model = User
        fields = ('password', 'username', 'email',)
        
#NOT IN USE
class UserProfileForm(UserForm):
    #script for styling the form
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

    class Meta:
        model = Member
        fields = ('username','password', 'email',)
        
class SearchForm(forms.Form):
    #text box for the user to enter the value to search
    search = forms.CharField(max_length=128)
    #drop down box for the user to choose which list they want to search
    options = forms.ChoiceField(choices=[("1","Genre"), ("2","Title"), ("3","Author",), ("4","ISBN")], help_text="Choose what to search.")

    #script for styling the form
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})


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