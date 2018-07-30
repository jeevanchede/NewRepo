# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime, timedelta
# Create your models here.

class User(models.Model):
	name = models.CharField(max_length=50)
	username = models.CharField(max_length=50,blank=False)
	password = models.CharField(max_length=50,blank=False)
	email = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=50)
	MY_CHOICES = [('student', 'student'), ('librarian', 'librarian')]
	typeuser= models.CharField(max_length=50,choices=MY_CHOICES)


	def __str__(self):
		return self.username+" "+self.password

class Books(models.Model):
	name = models.CharField(max_length=50)
	author = models.CharField(max_length=50)
	#no_of_copies = models.CharField(max_length=50)
	no_of_copies = models.IntegerField(default=5)
	summary = models.CharField(max_length=50)



	def __str__(self):
		return self.name+" "+self.author+" "	


def get_deadline():
    return datetime.today() + timedelta(days=7)

class Issue_Table(models.Model):
	Book_name=models.CharField(max_length=50)
	student_name=models.CharField(max_length=50)
	MY_CHOICES = [('Available','Available'),('Booked','Booked'),('Issued','Issued')]
	status=models.CharField(max_length=50,choices=MY_CHOICES)
	issue_date=models.DateField()
	return_date=models.DateField()

	def __str__(self):
		return self.Book_name+" "+self.student_name+" "+self.status	

class Return_Table(models.Model):
	Book_name=models.CharField(max_length=50)
	student_name=models.CharField(max_length=50)
	MY_CHOICES = [('Available','Available'),('Booked','Booked'),('Issued','Issued')]
	status=models.CharField(max_length=50,choices=MY_CHOICES)
	issue_date=models.DateField()
	return_date=models.DateField()

	def __str__(self):
		return self.Book_name+" "+self.student_name+" "+self.status	


class Book_history_ReturnedBooks(models.Model):
	Book_name=models.CharField(max_length=50)
	student_name=models.CharField(max_length=50,default="jeevan")
	issue_date=models.DateField()
	return_date=models.DateField()

	def __str__(self):
		return self.Book_name+" "+self.student_name	


