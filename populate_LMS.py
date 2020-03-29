import os
import random
import string
os.environ.setdefault('DJANGO_SETTINGS_MODULE','LMS_project.settings')

import django
import csv
django.setup()
from LMS.models import Member, Staff, Category, ISBN, Book

def populate():
    #Create the Categories
    cat_names = ["General Works", "Philosophy", "Religion", "Social Sciences", "Culture", "Natural Sciences", "Applied Sciences", "Recreation", "Fiction & Literature", "History & Geography"]
    cat_views = [425,365,227,589,363,741,691,123,966,314]
    for cat in enumerate(cat_names):
        p = Category(pk_num=cat[0], name=cat[1], views = cat_views[cat[0]], manager=None)
        p.save()
        
    
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