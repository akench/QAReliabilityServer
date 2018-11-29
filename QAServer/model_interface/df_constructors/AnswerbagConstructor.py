from pandas import DataFrame
from regression import regression, calculate_features
from regression.format_answers import FormatAnswer

class AnswerbagConstructor():
    def __init__(self, answer):
        self.answer = answer

    def get_features_df(self):
        ## NECESSARY FEATURES from FormatAnswer:
        # avg_word_sentence, num_misspelled, bin_taboo, grammar_check
        text = self.answer['answer']
        _, IDF, entropy, polarity, subjectivity = calculate_features.get_all_scores(text)
        
        formatter = FormatAnswer(text)
        avg_word_sentence = formatter.average_words_per_sentence()
        num_misspelled = formatter.number_of_misspelled_words()
        bin_taboo = formatter.check_for_profanity()
        grammar_check = 0 # formatter.grammar_checking()

        df_data = {
            'Answers': [self.answer['answer']],
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