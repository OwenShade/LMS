# Generated by Django 2.2.3 on 2020-03-29 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='reg_library',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='reg_library',
        ),
        migrations.AlterField(
            model_name='book',
            name='location',
            field=models.CharField(max_length=16),
        ),
        migrations.DeleteModel(
            name='Library',
        ),
    ]
