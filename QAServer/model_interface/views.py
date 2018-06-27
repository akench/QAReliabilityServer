import json
import random
import string

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from caching.models import Report

hrefs_collected = set()


def collect_data(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('''This endpoint only accepts POST requests. \
			\rTry again with a JSON payload.''')
    body = json.loads(request.body)
    href = body['href']

    if href not in hrefs_collected and has_valid_answers(body):
        # Create the filename from the first ten words of the question
        filename = 'collection/'
        filename += '_'.join(body['brainly_data']
                             ['question'].split(maxsplit=10)[:10])
        # filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        filename += '.json'
        with open(filename, 'w') as f:
            json.dump(body, f)
        hrefs_collected.add(href)

        print('SAVED FILE: ' + filename)
    else:
        print('NOT SAVING')

    results = get_inference('', '')
    return JsonResponse(results)

def generate_report(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('''This endpoint only accepts POST requests. \
			\rTry again with a JSON payload.''')

    # Parse JSON body
    body = json.loads(request.body)
    print(body)
    try:
        # site = body['site']
        # url = body['url']
        question = body['question']
        answer = body['answer']
        # cache = body['cache']
    except KeyError:
        return HttpResponseBadRequest('''Incomplete request, \
                try again with all of the following parameters: 	\
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

def has_valid_answers(request_body):
    """
    Checks if there are any answers that are not
    just one/few-word answers.
    """

    answers = request_body['brainly_data']['all_answers']

    for answer in answers:
        answer = answer['text'].strip()
        print(answer)
        if answer.count(" ") > 2:
            return True

    # Return false to indicate that the entire question is
    # useless since there is no useful data
    return False