# Generated by Django 2.2.3 on 2020-03-23 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0003_auto_20200322_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='category',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]