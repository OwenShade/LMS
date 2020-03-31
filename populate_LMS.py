import os
import random
import string
os.environ.setdefault('DJANGO_SETTINGS_MODULE','LMS_project.settings')

import django
import csv
django.setup()
from LMS.models import Member, Staff, Category, ISBN, Book
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

def populate():
    #Create the Categories
    cat_names = ["General Works", "Philosophy", "Religion", "Social Sciences", "Culture", "Natural Sciences", "Applied Sciences", "Recreation", "Fiction & Literature", "History & Geography"]
    cat_views = [425,365,227,589,363,741,691,123,966,314]
    for cat in enumerate(cat_names):
        p = Category(pk_num=cat[0], name=cat[1], views = cat_views[cat[0]], manager=None)
        p.save()
    
    #Create groups and admin user
    Group.objects.get_or_create(name='admin')
    Group.objects.get_or_create(name='staff')
    Group.objects.get_or_create(name='member')
    user = User.objects.create_user('admin', 'admin@admin.com', 'admin')
    group = Group.objects.get(name='admin')
    user.groups.add(group)

    # At this point, user is a User object that has already been saved
    # to the database. You can continue to change its attributes
    # if you want to change other fields.
    user.last_name = 'Lennon'
    user.save()
    
    #Add the ISBN of books
    with open('book.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            p = ISBN(ISBN=int(row['isbn']), title=row['title'], author=row['author'], genre=row['genre'], category=Category.objects.get(pk_num=int(row['categoryid'])),views=random.randrange(75))
            p.save()
            
    #Add Books
    for key in enumerate(ISBN.objects.all()):
        b = Book(isbn=key[1], location=random.choice(string.ascii_letters[26:])+str(random.randrange(20)))
        b.save()
if __name__ == '__main__':
    print('Starting LMS population script...')
populate()