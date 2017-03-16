from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from random import randint

class Account (models.Model):
	account_no = models.CharField(max_length=6,blank=False,unique=True)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	balance = models.IntegerField(default=0)
	atm_pin = models.CharField(max_length=4,blank=False,default=randint(1000,9999))


