from django.db import models
import re

class User_Manager(models.Manager):
    def registration_validator(self, form_data):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if len(form_data['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters."
        if len(form_data['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if not email_regex.match(form_data['reg_email']): 
            errors['reg_email'] = "Invalid email address."
        if len(form_data['reg_password']) < 8:
            errors["reg_password"] = "Password requires at least 8 charaters."
        if form_data['reg_password'] != form_data['confirm_pw']:
            errors["confirm_pw"] = "Password must match."
        return errors

    def login_validator(self, form_data):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if not email_regex.match(form_data['log_email']): 
            errors['log_email'] = "please enter valid email address."
        if len(form_data['log_password']) == 0:
            errors["log_password"] = "Please enter Password."
        return errors

    def edit_validator(self, form_data):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if len(form_data['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters."
        if len(form_data['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if not email_regex.match(form_data['reg_email']): 
            errors['reg_email'] = "Invalid email address."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = User_Manager()

class ProductManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['product_name']) < 3:
            errors["product_name"] = "Product name should be at least 3 characters"
        if len(postData['description']) < 10:
            errors["description"] = "Description of quote should be at least 10 characters"
        return errors

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, related_name="products", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()