from django.db import models
import re

from django.db.models.deletion import CASCADE

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters!"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters!"
        if not EMAIL_REGEX.match(postData['email']): 
            errors['email'] = ("Invalid email address!")
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters!"
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Passwords do not match!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    drinks = models.ImageField(null=True, blank=True, upload_to="images/")
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # drinks_created = list of drinks created by this user

class DrinkManager(models.Manager):
    def drink_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors['name'] = "Name should be at least 2 characters!"
        if not isinstance(postData['price'], float):
            errors['price'] = "Please use digits and decimals only."
        elif (postData['price']).find(".")>0:
            if len((postData['price']).split(".")[1])!=2:
                errors['price'] = "There should be two digits to the right of the decimal."
        if len(postData['desc']) < 1:
            errors['desc'] = "Description can not be empty!"
        return errors

class Drink(models.Model):
    name = models.CharField(max_length=255)
    price =  models.DecimalField(decimal_places=2, max_digits=5)
    desc = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    content_creator = models.ForeignKey(User, related_name="drinks_created", on_delete = models.CASCADE)
    profile_item = models.ManyToManyField(User, related_name="all_profile_items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = DrinkManager()

class Order(models.Model):
    order_customer = models.ForeignKey(User, related_name="one_user", on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderDetail(models.Model):
    order_number= models.ForeignKey(Order, related_name="order_details", on_delete=models.CASCADE)
    drinks = models.ManyToManyField(Drink, related_name="details")
    quantity = models.IntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=6)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)