from rest_framework import serializers
from .models import Account
from django.contrib.auth.models import User

class AccountSerializer(serializers.ModelSerializer):

	class Meta:
		model = Account
		fields = ['account_no','balance']

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ['username','first_name','last_name']