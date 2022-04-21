from calendar import prmonth
from pyexpat import model
import re
from django.db import models
import uuid

# Create your models here.

class User(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    username = models.CharField(max_length=10)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    password = models.CharField(max_length=129)

class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    text_body = models.CharField(max_length=300, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    # user_id = models.UUIDField(default=uuid.uuid4, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment = models.UUIDField('self', null=True)