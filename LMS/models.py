from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import date, timedelta

#initialises the types and relationships between different fields in the Member model
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    book_limit = models.IntegerField(default=10)
    date_reg = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

#initialises the types and relationships between different fields in the staff model
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=128)
    phone = models.IntegerField()
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Staff"

#initialises the types and relationships between different fields in the Category model
class Category(models.Model):
    pk_num = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    views = models.IntegerField(default=0)
    manager = models.ForeignKey(Staff, on_delete=models.SET(None), blank=True, null=True)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.views < 0:
            self.views = 0
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

#initialises the types and relationships between different fields in the ISBN model
class ISBN(models.Model):
    ISBN = models.IntegerField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    genre = models.CharField(max_length=128)
    views = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if self.views < 0:
            self.views = 0
        super(ISBN, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name_plural = "ISBNs"

#initialises the types and relationships between different fields in the book model
class Book(models.Model):
    pk_num = models.AutoField(primary_key=True)
    isbn = models.ForeignKey(ISBN, on_delete=models.CASCADE)
    location = models.CharField(blank=False, max_length=16)
    taken_out = models.ForeignKey(Member, on_delete=models.SET(None), blank=True, null=True)
    loan_until = models.DateField(default=None, blank=True, null=True)
    back_in = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if self.taken_out != None and self.loan_until == None:
            self.loan_until = date.today() + timedelta(days=30)
            self.back_in = False
        super(Book, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.isbn)
