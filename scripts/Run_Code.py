import csv as csv
from FormatQuestions import FormatQuestions
protocol_list = ['num_words', 'num_characters', 'num_misspelled', 'bin_start_interrogative', 'bin_end_qmark',
                 'num_interrogative', 'bin_start_small', 'avg_word_sentence', 'num_sentences', 'bin_url',
                 'readability_score', 'num_punctuations', 'bin_taboo', 'grammar_check']
func_list = ['get_total_words', 'get_total_number_of_characters', 'number_of_misspelled_words',
             'check_interrogative_start', 'check_question_mark_end', 'number_of_interrogative_words',
             'check_small_letter_start', 'average_words_per_sentence', 'get_number_of_sentences',
             'check_if_url_present', 'get_readability_score', 'number_of_punctuation_marks', 'check_for_profanity' , 'grammar_checking']
with open('input.csv', 'r',  encoding='ISO-8859-1',) as f:
    with open('output.csv', 'w', encoding='ISO-8859-1', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        reader = csv.reader(f)
        row = next(reader)  # pass the file to our csv reader
        new_row = row
        new_row = row + protocol_list
        wr.writerow(new_row)
        #count = 1

        for row in reader:
            new_row = row
            if len(row) < 1:
                continue

            obj = FormatQuestions(row[0])
            for func in func_list:
                method = getattr(obj, func)
                new_row.append(str(method()))
            wr.writerow(new_row)
