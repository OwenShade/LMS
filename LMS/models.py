from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Library(models.Model):
    pk_num = models.IntegerField(unique=True)
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name
    
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    pk_num = models.CharField(max_length=128, unique=True)
    reg_library = models.ForeignKey(Library, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    book_limit = models.IntegerField(max_length=20)
    email = models.EmailField()
    date_reg = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    pk_num = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128)
    reg_library = models.ForeignKey(Library, on_delete=models.CASCADE)
    role = models.CharField(max_length=128)
    phone = models.IntegerField(max_length=15)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    pk_num = models.IntegerField(max_length=11, unique=True)
    name = models.CharField(max_length=128)
    manager = models.ForeignKey(Staff, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class ISBN(models.Model):
    pk_num = models.IntegerField(max_length=13, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    genre = models.CharField(max_length=128)
    
    def __str__(self):
        return self.pk_num
    
class Book(models.Model):
    pk_num = models.IntegerField(unique=True)
    isbn = models.ForeignKey(ISBN, on_delete=models.CASCADE)
    location = models.ForeignKey(Library, on_delete=models.CASCADE)
    taken_out = models.ForeignKey(Member, on_delete=models.SET(None), default=None, null=True)
    
    def __str__(self):
        return self.pk_num
