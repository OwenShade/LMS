import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','LMS_project.settings')

import django
import csv
django.setup()
from LMS.models import ISBN

def populate():
    with open('book.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            p = ISBN(pk_num=row['ISBN'], title=row['Title'], author=row['Author'], genre=row['Genre'], category=row['CategoryID'])
            p.save()
            
            
if __name__ == '__main__':
    print('Starting Rango population script...')
populate()