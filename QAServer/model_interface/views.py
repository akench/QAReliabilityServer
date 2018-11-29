import json
from enum import Enum
from pandas import DataFrame
from regression import regression, calculate_features
from regression.format_answers import FormatAnswer
from model_interface.df_constructors.BrainlyConstructor import BrainlyConstructor
from django.http import JsonResponse, HttpResponseBadRequest
from model_interface.scrapers import AnswerbagScraper

class SiteType(Enum):
    Brainly = 0
    Answerbag = 1

def generate_report(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('''This endpoint only accepts POST requests. \
			\rTry again with a JSON payload.''')

    # Parse JSON body
    print('got request')
    all_answers = None
    body = json.loads(request.body)
    if body['brainly_data']:
        all_answers = body['brainly_data']['all_answers']
        for answer in all_answers:
            answer['inference'] = get_inference(answer)
    elif body['answerbag_data']:
        all_answers = body['answerbag_data']['all_answers']
        for answer in all_answers:
            scraper = AnswerbagScraper(answer['username'])
            answer['user_followers'], answer['user_following'] = scraper.get_user_stats()
    else:
        pass

    return JsonResponse({'all_answers': all_answers})

#########################
#   HELPER FUNCTIONS    #
#########################

def get_inference(answer, site_type=SiteType.Brainly):
    scores = None
    if site_type == SiteType.Brainly:
        dataframe = BrainlyConstructor(answer).get_features_df()
        scores = get_final_scores(dataframe, models=regression.BrainlyModels)
    elif site_type == SiteType.Answerbag:
        dataframe = BrainlyConstructor(answer).get_features_df()
        scores = get_final_scores(dataframe, models=regression.BrainlyModels)
    
    ret_data = {
        'clearness': scores['Clear_1 %'][0],
        'credibility': scores['Credible_1 %'][0],
        'completeness': scores['Complete_1 %'][0],
        'correctness': scores['Correct_1 %'][0]
    }
    ret_data['overall'] = compute_overall_score(ret_data)
    print(ret_data)

    return ret_data

def compute_overall_score(scores):
    clear = scores['clearness']
    credible = scores['credibility']
    complete = scores['completeness']
    correct = scores['correctness']

    return (clear + credible + complete + correct) / 4

def get_final_scores(dataframe, models=regression.BrainlyModels):
    clear_model = models.Clear_model
    credible_model = models.Credible_model
    complete_model = models.Complete_model
    correct_model = models.Correct_model

    clear_data=regression.test_function(models.X_Clear, 'Clear_1', clear_model, dataframe)
    complete_data=regression.test_function(models.X_Complete, 'Complete_1', complete_model, clear_data)
    credible_data=regression.test_function(models.X_Credible, 'Credible_1', credible_model, complete_data)
    correct_data=regression.test_function(models.X_Correct, 'Correct_1', correct_model, credible_data)

    regression.calc_percent(correct_data,'Correct_1')
    regression.calc_percent(correct_data,'Credible_1')
    regression.calc_percent(correct_data,'Complete_1')
    regression.calc_percent(correct_data,'Clear_1')

    final_data = correct_data[[ 'Clear_1 %', 'Credible_1 %', 'Complete_1 %', 'Correct_1 %' ]]

    return final_data