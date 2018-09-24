from __future__ import unicode_literals
from django.db import models
import re

letters_regex = re.compile(r'^[a-zA-Z]+$')
email_regex = re.compile(r'^[a-zA-z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # validate the length and characters of the first name
        if len(postData["first_name"]) < 2:
            errors["first_name_len"] = "First name must be at least 2 letters."
        if not letters_regex.match(postData["first_name"]):
            errors["first_name_regex"] = "First name may only contain letters."
        # validate the length and characters of the last name
        if len(postData["last_name"]) < 2:
            errors["last_name_len"] = "Last name must be at least 2 letters."
        if not letters_regex.match(postData["last_name"]):
            errors["last_name_regex"] = "Last name may only contain letters."
        # validate the email address
        if not email_regex.match(postData["email"]):
            errors["email_regex"] = "Please enter a valid email address."
        # validate the length of the password
        if len(postData["password"]) < 8:
            errors["password"] = "Password must be at least 8 characters."
        # validate that both passwords are the same
        if postData["password_confirm"] != postData["password"]:
            errors["password_confirm"] = "Passwords must match."
        return errors
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager() # call the validator