from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User



# Create your models here.


class Books(models.Model):
    #extending from the inbuilt model TextChoices.
    class BookStatusChoices(models.TextChoices):
        AVAILABLE = "AV", ("Available")
        UNAVAILABLE = "UNAV", ("Unavailable")
        BOOKED = "BK", ("Booked")

    title = models.CharField( max_length=50)
    author = models.CharField(max_length=50)
    copy_number = models.IntegerField()
    subject_area  = models.CharField(max_length=50)
    publication_date = models.DateField()
    status = models.CharField(max_length=20, default="AV", choices=BookStatusChoices.choices)
    category = models.CharField(max_length=100, default="Engineering")
    
   

class Borrowed_books(models.Model):
    
    class ReturnStatusChoices(models.TextChoices):
        BOOKED = "BK", ("Booked")
        TAKEN = "TK", ("Taken")
        RETURNED = "RT", ("Returned")
        
    book = models.ForeignKey(Books,related_name= 'titles', on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name = 'first_names',on_delete = models.CASCADE,max_length=100)
    pickup_date = models.DateTimeField(null=True)
    return_date = models.DateTimeField(null=True)
    fine = models.IntegerField(null=True, blank=True)
    return_status = models.CharField(max_length=15, default="BK", choices=ReturnStatusChoices.choices)

    
    

