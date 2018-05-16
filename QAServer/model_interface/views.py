import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from caching.models import Report

# Create your views here.
def generate_report(request):
	if request.method != 'POST':
		return HttpResponseBadRequest('''This endpoint only accepts POST requests. \
			\rTry again with a JSON payload.''')

	# Parse JSON body
	body = json.loads(request.body)
	print(body)
	try:
		site = body['site']
		url = body['url']
		question = body['question']
		answer = body['answer']
		cache = body['cache']
	except KeyError as error:
		return HttpResponseBadRequest('''Incomplete request, try again with all of the following parameters: 	\
			\r1) site (string) : the website from which the QA originates 										\
			\r2) url (string) : the raw url referring to the question	 										\
			\r3) question (string) : the question being asked 													\
			\r4) answer (string) : the answer to the question 													\
			\r5) cache (boolean) : whether or not the report for this url should be cached''')					

	# Do something to get results
	results = get_inference(question, answer)
	return JsonResponse(results)

def get_inference(question, answer):
	# I don't remember what the specific statistics were, so they'll
	# be modified as necessary later.
	ret_data = {
		'error': False,
		'statistics': {
			'reliability': 50,
			'ambiguity': 25,
			'brevity': 80,
			'thoroughness': 0
		}
	}
	return ret_data