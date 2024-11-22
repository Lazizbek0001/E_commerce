from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
# Create your models here.
