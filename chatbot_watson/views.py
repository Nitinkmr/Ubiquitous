## bank DB on https://api.myjson.com/bins/hvyw7
import json, requests, random, re
from pprint import pprint
import urllib2
from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator# Create your views here.

from watson_developer_cloud import ConversationV1

conversation = ConversationV1(
	    username='e892b0dd-dbd3-4626-a9c4-d8e8dba79ef0',
	    password='g5sH0CQezT5f',
	    version='2017-02-03')

# replace with your own workspace_id
workspace_id = '9e44a13b-3ed7-4991-9a1e-b17b842a4055'

global context
context = None

PLANS = {'3G':[],'2G':[],'FULL TALKTIME':[],'SPECIAL':[],'ROAMING':[],'TOP_UP':[]}
PLAN_TYPE_MAPPING = {'1':'3G','2':'2G','3':'FULL TALKTIME','4':'SPECIAL','5':'TOP_UP','6':'ROAMING'}
OPERATOR_MAPPING = {'vodafone':'22',
					 'airtel':'28',
					 'aircel':'1',
					 'bsnl':'3',
					 #'tata docomo gsm':'17',
					 #'tata docomo cdma':'18',
					 #'reliance gsm':'13',
					 #'reliance cdma':'12',
					 'mts':'10',
					 'uninor':'19',
					 'videocon':'5',
					 'idea':'8',
					 'mtnl':'20',}
					 #'virgin gsm':'17',
					 #'virgin cdma':'18'}

def get_operator_code(operator):
	for key in OPERATOR_MAPPING.keys():
		if  key in operator.lower():
			return OPERATOR_MAPPING[key]

def get_plans_clean(response):
	for plan in response:
		detail=plan['Detail']
		if '3G' in detail:
			PLANS['3G'].append(plan)
		if '2G' in detail:
			PLANS['2G'].append(plan)
		if 'Full Talktime' in detail:
			PLANS['FULL TALKTIME'].append(plan)
		if 'Special' in detail:
			PLANS['SPECIAL'].append(plan)
		if 'Topup' in detail:
			PLANS['TOP_UP'].append(plan)
		if 'roaming' in detail:
			PLANS['ROAMING'].append(plan)

def get_plan(operator,context):
	response =  json.loads(urllib2.urlopen("https://joloapi.com/api/findplan.php?userid=nitinkmr&key=469150899121702&opt="+ get_operator_code(operator) + "&cir=1&type=json").read())				
	if 'recharge_plans' not in context:
		context['recharge_plans'] = {}

	if operator not in context['recharge_plans']:
		context['recharge_plans'][operator] = response
	get_plans_clean(response)

def post_facebook_message(fbid, recevied_message):             
	
	#context = request.session.get('context')
	print fbid
	global context
	# when first user comes 
	if context is None:
		context = {}
		context[fbid] = None
	


	# if a new user comes in 
	if fbid not in context:
		context[fbid] = {}

	try:
		response = conversation.message(workspace_id=workspace_id, message_input={'text':str(recevied_message)},context = context[fbid])
		context[fbid] = response['context']
		
		print context
		post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAFo3cregLIBAKwqzPX5TZCxBCcLBH2LiOqYMYI5vvZBRhVayhwH78XjsreShgXDNdxA8hAP1LZCDROM3a4fxGSmpXLJVZCbiyujuMq5j1Vfwrr98vDguIYf5z4uDlryjPYh250SegmaILoC6mbWlO6VcUr9z3FDF2UumkIXawZDZD'
		
		for mssg in response['output']['text']:
				response_msg = json.dumps({"recipient":{"id":fbid},"message":{"text":str(mssg)}})    
				status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
		
		if 'mobile_no' in response['context']  and response['output']['nodes_visited'][0] == 'save_plan_selected':
			print "saved"
			plan_selected = context[fbid]['plan_selected']
			mobile_no = response['context']['mobile_no']
			operator_url = "http://apilayer.net/api/validate?access_key=eed41e844d0c218d041d74594ccb6844&number=" + str(mobile_no) + "&country_code=IN&format=1"
			operator_data = urllib2.urlopen(operator_url)
			operator_data = json.loads(operator_data.read())
			if operator_data['valid']:
				operator = operator_data['carrier']
				context[fbid]['telecom_operator'] = str(operator)
				get_plan(str(operator),context)
				for plans in PLANS[PLAN_TYPE_MAPPING[plan_selected]]:
					response_msg = json.dumps({"recipient":{"id":fbid},"message":{"text":plans['Detail']}})	
					status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)				
			else:
				response_msg = json.dumps({"recipient":{"id":fbid},"message":{"text": "Invalid Mobile Numbers"}})    
				status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
				context[fbid]['telecom_operator'] = None			
		
	except Exception as e:
		print "error" + str(e)


class bot(generic.View):
	
	def get(self, request, *args, **kwargs):
	       

	      #  print "get request"
	        if self.request.GET['hub.verify_token'] == '123456':
	            return HttpResponse(self.request.GET['hub.challenge'])
	        else:
	            return HttpResponse('Error, invalid token')
	
	@method_decorator(csrf_exempt)
    	def dispatch(self, request, *args, **kwargs):
        	#print "dispatch "
        	return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
   	def post(self, request, *args, **kwargs):
	        # Converts the text payload into a python dictionary
	       # print "post request"
	        incoming_message = json.loads(self.request.body.decode('utf-8'))
	        # Facebook recommends going through every entry since they might send
	        # multiple messages in a single call during high load
	        for entry in incoming_message['entry']:
	            for message in entry['messaging']:
	                # Check to make sure the received call is a message call
	                # This might be delivery, optin, postback for other events 
	                if 'message' in message:
		                # Print the message to the terminal
		       #         pprint(message)     
		                post_facebook_message(message['sender']['id'], message['message']['text'])   
	        return HttpResponse()
