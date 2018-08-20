import json
from pandas import DataFrame
from regression import regression, calculate_features
from regression.format_answers import FormatAnswer
from django.http import JsonResponse, HttpResponseBadRequest

def generate_report(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('''This endpoint only accepts POST requests. \
			\rTry again with a JSON payload.''')

    # Parse JSON body
    body = json.loads(request.body)
    all_answers = body['brainly_data']['all_answers']
    for answer in all_answers:
        answer['inference'] = get_inference(answer)
    
    return JsonResponse({'all_answers': all_answers})


#########################
#   HELPER FUNCTIONS    #
#########################

def get_inference(answer):
    dataframe = get_features_df(answer)
    scores = get_final_scores(dataframe)
    
    ret_data = {
        'clearness': scores['Clear_1 %'][0],
        'credibility': scores['Credible_1 %'][0],
        'completeness': scores['Complete_1 %'][0],
        'correctness': scores['Correct_1 %'][0]
    }

    ret_data['overall'] = compute_overall_score(ret_data)

    return ret_data

def compute_overall_score(scores):
    clear = scores['clearness']
    credible = scores['credibility']
    complete = scores['completeness']
    correct = scores['correctness']

    return (clear + credible + complete + correct) / 4

def get_features_df(answer):
    ## NECESSARY FEATURES from FormatAnswer:
    # avg_word_sentence, num_misspelled, bin_taboo, grammar_check

    text = answer['text']
    _, IDF, entropy, polarity, subjectivity = calculate_features.get_all_scores(text)
    
    formatter = FormatAnswer(text)
    avg_word_sentence = formatter.average_words_per_sentence()
    num_misspelled = formatter.number_of_misspelled_words()
    bin_taboo = formatter.check_for_profanity()
    grammar_check = formatter.grammar_checking()

    df_data = {
        'Answers': [answer['text']],
        'rating': [answer['rating']],
        'num_upvotes': [answer['num_upvotes']],
        'num_thanks': [answer['num_thanks']],
        'avg_word_sentence': [avg_word_sentence],
        'num_misspelled': [num_misspelled],
        'bin_taboo': [bin_taboo],
        'grammar_check': [grammar_check],
        'Average IDF': [IDF],
        'Entropy': [entropy],
        'Polarity': [polarity],
        'Subjectivity': [subjectivity]
    }

    return DataFrame(data=df_data)

def get_final_scores(dataframe):
    clear_model = regression.Clear_model
    credible_model = regression.Credible_model
    complete_model = regression.Complete_model
    correct_model = regression.Correct_model

    clear_data=regression.test_function(regression.X_Clear, 'Clear_1', clear_model, dataframe)
    complete_data=regression.test_function(regression.X_Complete, 'Complete_1', complete_model, clear_data)
    credible_data=regression.test_function(regression.X_Credible, 'Credible_1', credible_model, complete_data)
    correct_data=regression.test_function(regression.X_Correct, 'Correct_1', correct_model, credible_data)

    regression.calc_percent(correct_data,'Correct_1')
    regression.calc_percent(correct_data,'Credible_1')
    regression.calc_percent(correct_data,'Complete_1')
    regression.calc_percent(correct_data,'Clear_1')

    final_data = correct_data[[ 'Clear_1 %', 'Credible_1 %', 'Complete_1 %', 'Correct_1 %' ]]

    return final_data