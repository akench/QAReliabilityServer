import json
from enum import Enum
from pandas import DataFrame
from regression import calculate_features
from regression.CQtool import get_regression_scores
from regression.format_answers import FormatAnswer
from django.http import JsonResponse, HttpResponseBadRequest
from model_interface.scrapers import AnswerbagScraper

def generate_report(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('''This endpoint only accepts POST requests. \
			\rTry again with a JSON payload.''')

    # Parse JSON body
    body = json.loads(request.body)
    all_answers = body['scraped']['all_answers']
    for answer in all_answers:
        answer['inference'] = get_inference(answer)

    print('done, returning')
    return JsonResponse({'all_answers': all_answers})

#########################
#   HELPER FUNCTIONS    #
#########################

def get_inference(answer):
    dataframe = get_features_df(answer)
    scores = get_regression_scores(dataframe)

    print(scores)
    return scores

def get_features_df(answer):
    ## NECESSARY FEATURES from FormatAnswer:
    # avg_word_sentence, num_misspelled, bin_taboo, grammar_check
    text = answer['content']
    _, IDF, entropy, polarity, subjectivity = calculate_features.get_all_scores(text)
    
    formatter = FormatAnswer(text)
    df_data = {
        'Content': [ text ],
        'Author': [ answer['author'] ],
        'Date': [ 0 ],
        'info_content': [ answer['info_content'] ],
        'info_author': [ answer['info_author'] ],
        'grammar_check': [ 0 ],
        'Average IDF': [ IDF ],
        'Entropy': [ entropy ],
        'Polarity': [ polarity ],
        'Subjectivity': [ subjectivity ]
    }

    protocol_list = ['num_words', 'num_characters', 'num_misspelled', 'bin_start_interrogative', 'bin_end_qmark',
        'num_interrogative', 'bin_start_small', 'avg_word_sentence', 'num_sentences', 'bin_url',
        'readability_score', 'num_punctuations', 'bin_taboo', 'grammar_check']
    formatanswers_func_list = ['get_total_words', 'get_total_number_of_characters', 'number_of_misspelled_words',
        'check_interrogative_start', 'check_question_mark_end', 'number_of_interrogative_words',
        'check_small_letter_start', 'average_words_per_sentence', 'get_number_of_sentences',
        'check_if_url_present', 'get_readability_score', 'number_of_punctuation_marks', 'check_for_profanity', 'grammar_check']

    for index, method_name in enumerate(formatanswers_func_list):
        runnable_method = getattr(formatter, method_name)
        df_data[protocol_list[index]] = [ float(runnable_method()) ]

    from pprint import pprint
    # pprint(df_data)

    return DataFrame(data=df_data)