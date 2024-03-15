from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404
# Create your models here.



class User(AbstractUser):
    type_user=models.CharField(max_length=200)
    



class Department (models.Model):
    department=models.CharField(max_length=100)
    def __str__(self):
        return self.department

class AddressOne(models.Model):
    address=models.CharField(max_length=100)
    def __str__(self):
        return self.address

class AddressTwo(models.Model):
    address=models.CharField(max_length=100)
    address_one = models.ForeignKey(AddressOne,on_delete=models.CASCADE)
    def __str__(self):
        return self.address

class Student (models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)  
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    address1=models.ForeignKey(AddressOne,on_delete=models.CASCADE)
    address2=models.ForeignKey(AddressTwo,on_delete=models.CASCADE)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    year=models.IntegerField()

class Empolyee(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)    
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    address1=models.ForeignKey(AddressOne,on_delete=models.CASCADE)
    address2=models.ForeignKey(AddressTwo,on_delete=models.CASCADE)
    job=models.CharField(max_length=100)

class Buses(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    number=models.IntegerField(max_length=10)
    phone=models.IntegerField(max_length=20)

class Lines(models.Model):
    name_of_line = models.CharField(max_length=100)
    address_one = models.ForeignKey(AddressOne,on_delete=models.CASCADE)
    address_two = models.ForeignKey(AddressTwo,on_delete=models.CASCADE) 
    round_trip= models.BooleanField()
    distance = models.IntegerField()
    time = models.TimeField()
    itinerary = models.JSONField(null=True,blank=True)

class Trips(models.Model):
    name_of_bus = models.ForeignKey(Buses,on_delete=models.CASCADE)
    name_of_line = models.ForeignKey(Lines,on_delete=models.CASCADE)
    started_at = models.TimeField()    
    flight_number = models.AutoField(primary_key=True)

    