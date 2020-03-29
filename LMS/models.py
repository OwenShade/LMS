from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
class Library(models.Model):
    pk_num = models.IntegerField(unique=True)
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Libraries"
    
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    reg_library = models.ForeignKey(Library, on_delete=models.CASCADE, help_text="Registered Library")
    book_limit = models.IntegerField(default=10)
    date_reg = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    reg_library = models.ForeignKey(Library, on_delete=models.CASCADE)
    role = models.CharField(max_length=128)
    phone = models.IntegerField()
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Staff"
    
class Category(models.Model):
    pk_num = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    views = models.IntegerField(default=0)
    manager = models.ForeignKey(Staff, on_delete=models.SET(None), blank=True, null=True)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        
class ISBN(models.Model):
    ISBN = models.IntegerField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    genre = models.CharField(max_length=128)
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name_plural = "ISBNs"
    
class Book(models.Model):
    pk_num = models.AutoField(primary_key=True)
    isbn = models.ForeignKey(ISBN, on_delete=models.CASCADE)
    location = models.ForeignKey(Library, on_delete=models.CASCADE)
    taken_out = models.ForeignKey(Member, on_delete=models.SET(None), blank=True, null=True)
    
    def __str__(self):
        return str(self.isbn)
