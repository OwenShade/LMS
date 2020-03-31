from django.contrib import admin
from LMS.models import *
# created models to define hierachies and things to do with the books stored in the library
admin.site.register(Staff)
admin.site.register(Member)
admin.site.register(ISBN)
admin.site.register(Book)
admin.site.register(Category)