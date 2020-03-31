from django.contrib import admin
from django.contrib.admin.models import LogEntry

from LMS.models import *
# Register your models here.
admin.site.register(Staff)
admin.site.register(Member)
admin.site.register(ISBN)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(LogEntry)