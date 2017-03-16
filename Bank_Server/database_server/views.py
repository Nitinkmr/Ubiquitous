from django.shortcuts import render
from .models import Account
# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AccountSerializer,UserSerializer


@api_view(['GET'])
def validate_account(request):
	if 'account_no' not in request.query_params:
		return Response({'success':False,'message':'Missing account number'},status=status.HTTP_400_BAD_REQUEST)
	if Account.objects.filter(account_no=request.query_params['account_no']).exists():
		return Response({'success':True,'message':'Account Exists'},status=status.HTTP_200_OK)
	else:
		return Response({'success':True,'message':'No such account'},status=status.HTTP_200_OK)

@api_view(['POST'])
def get_details(request):
	data = request.query_params
	print data
	if 'account_no' not in data or 'pin' not in data:
		 return Response({'success':False,'message':'Missing Parameters'},status=status.HTTP_400_BAD_REQUEST)
	account = Account.objects.get(account_no=data['account_no'])
	if account.atm_pin == data['pin']:
		serializer = AccountSerializer(account)
		return Response(serializer.data,status=status.HTTP_200_OK)
	else:
		return Response({'success':False,'message':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)


