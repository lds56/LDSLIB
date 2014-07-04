from django.db import models
from django.core.exceptions import ValidationError

class Book(models.Model):
	CATAGORY_CHOICE = (
		('Art', 'Art'),
		('Bussiness', 'Bussiness'),
		('Computer', 'Computer'),
		('Food', 'Food'),
		('Education', 'Education'),
		('Engineering', 'Engineering'),
		('Science', 'Science'),
		('Math', 'Math'),
		('Other', 'Other')
	)
	title = models.CharField(max_length = 50)
	author = models.CharField(max_length = 20)
	publisher = models.CharField(max_length = 30, blank = True, verbose_name = 'Press')
	ISBN = models.CharField(max_length = 40, primary_key = True)
	index = models.CharField(max_length = 20)
	edition = models.IntegerField(null = True)
	catagory = models.CharField(max_length = 15, choices = CATAGORY_CHOICE, default = 'OTR')
	publish_date = models.DateField()
	inventory = models.IntegerField()
	total = models.IntegerField()
	lend_time = models.IntegerField(default = 0)
	price = models.CharField(max_length = 10)
	description = models.CharField(max_length = 1000)
	#pic_path = models.CharField(max_length = 50)

class Books(models.Model):
	title = models.CharField(max_length = 30)
	author = models.CharField(max_length = 20)
	publisher = models.CharField(max_length = 30, null = True, verbose_name = 'Press')
	ISBN = models.CharField(max_length = 20, primary_key = True)
	index = models.CharField(max_length = 20)
	edition = models.IntegerField(blank=True)
	
class Book_record(models.Model):
	book_ISBN = models.CharField(max_length = 40)
	book_title = models.CharField(max_length = 50)
	return_date = models.DateField()

class User_info(models.Model):
	username = models.CharField(max_length = 30, primary_key = True)
	email = models.CharField(max_length = 40)
	country = models.CharField(max_length = 20)
	city = models.CharField(max_length = 20)
	code = models.CharField(max_length = 20)
	number = models.CharField(max_length = 20)
	address = models.CharField(max_length = 40)
	company = models.CharField(max_length = 20)
	mybooks = models.ManyToManyField(Book_record, blank = True)

#class Tag(models.Model):
#	ISBN = models.ForeignKey(Book)
	  
