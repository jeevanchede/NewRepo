# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-23 14:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_book_history_returnedbooks_student_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='book_history_returnedbooks',
            name='student_name',
            field=models.CharField(default='jeevan', max_length=50),
        ),
    ]
