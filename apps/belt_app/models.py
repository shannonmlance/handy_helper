from __future__ import unicode_literals
from django.db import models
from apps.login_app.models import User
import re

class JobManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        # validate the length of the title
        if len(postData["title"]) < 4:
            errors["title_len"] = "Title must be more than 3 characters."
        # validate the length of the description
        if len(postData["description"]) < 11:
            errors["description_len"] = "Description must be more than 10 characters."
        # validate the length of the location
        if len(postData["location"]) < 1:
            errors["location_len"] = "Location must not be blank."
        return errors

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    user_posted = models.ForeignKey(User, related_name="job_posted")
    user_worked = models.ForeignKey(User, related_name="job_worked")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = JobManager() # call the validator