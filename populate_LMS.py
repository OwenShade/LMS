import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE','LMS_project.settings')

import django
import csv
django.setup()
from LMS.models import Library, Member, Staff, Category, ISBN, Book

def populate():
    #Create the Library
    p = Library(pk_num=1, name="Oakwood Library", address="G12 6TY")
    p.save()
    
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
            p = ISBN(ISBN=int(row['isbn']), title=row['title'], author=row['author'], genre=row['genre'], category=Category.objects.get(pk_num=int(row['categoryid'])))
            p.save()
            
    #Add Books
    for key in enumerate(ISBN.objects.all()):
        b = Book(pk_num=key[0], isbn=key[1], location=Library.objects.get(pk_num=1),views = random.randrange(100))
        b.save()
if __name__ == '__main__':
    print('Starting LMS population script...')
populate()