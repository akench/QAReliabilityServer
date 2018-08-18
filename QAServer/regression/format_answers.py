# download bad_words.txt from https://github.com/jared-mess/profanity-filter
import re
import language_check
from autocorrect import spell
from functools import reduce

# classVariable #using corpus from: https://github.com/jared-mess/profanity-filter
BAD_WORDS = set(line.strip('\n') for line in open('bad_words.txt'))
TOOL = language_check.LanguageTool('en-US')

class FormatAnswer:

    def __init__(self, input_string):
        self.input_string = input_string
        # self.set_bad_words(bad_words_file)

        self.sentences = None
        self.number_of_sentences = None
        self.words_in_sentences = None
        self.number_of_words_in_sentences = None
        self.misspelled_words = None
        self.readability_score = 0
        self.total_words = None
        self.total_number_of_characters = None
        self.total_number_of_characters_in_words = None

        self.INTERROGATIVE_WORDS = set(['what', 'where', 'when', 'who', 'whom', 'why', 'how'])

    def set_bad_words(self, bad_words_file):
        if 'BAD_WORDS' not in globals():
            bad_words_file = open(bad_words_file, 'r')
            global BAD_WORDS
            BAD_WORDS = set(line.strip('\n') for line in bad_words_file)

    def get_sentences(self):
        if self.sentences == None:
            self.sentences = list(filter(None, re.split("[!.?]+", self.input_string)))
        return self.sentences

    def get_words_in_sentences(self):
        if self.words_in_sentences == None:
            result = []
            for sentence in self.get_sentences():
                result.append(re.findall(r"[a-zA-Z0-9']+", sentence))
            self.words_in_sentences = result
        return self.words_in_sentences

    def get_number_of_words_in_sentences(self):
        if self.number_of_words_in_sentences == None:
            self.number_of_words_in_sentences = list(map(lambda x: len(x), self.get_words_in_sentences()))
        return self.number_of_words_in_sentences

    def get_total_words(self):
        if self.total_words == None:
            if len(self.get_number_of_words_in_sentences()) > 0:                
                self.total_words = reduce(lambda x, y: x + y, self.get_number_of_words_in_sentences())               
            else:
                self.total_words = 0
        return self.total_words

    def get_total_number_of_characters(self):
        if self.total_number_of_characters == None:
            self.total_number_of_characters = len(self.input_string) - self.input_string.count(' ')
        return self.total_number_of_characters

    def check_for_profanity(self):
        words_in_sentences = self.get_words_in_sentences()
        for sentence in words_in_sentences:
            for word in sentence:
                if word.lower() in BAD_WORDS:
                    return 1
        else:
            return 0

    def check_interrogative_start(self):
        words_in_sentences = self.get_words_in_sentences()
        if words_in_sentences != [] and words_in_sentences[0] != [] \
                and words_in_sentences[0][0].lower() in self.INTERROGATIVE_WORDS:
            return 1
        else:
            return 0

    def check_question_mark_end(self):
        if re.search('.*\?$', self.input_string) != None:
            return 1
        else:
            return 0

    def number_of_interrogative_words(self):
        result = 0
        words_in_sentences = self.get_words_in_sentences()
        for sentence in words_in_sentences:
            for word in sentence:
                if word.lower() in self.INTERROGATIVE_WORDS:
                    result = result + 1

        return result

    def check_small_letter_start(self):
        if re.search('^[a-z]', self.input_string) != None:
            return 1
        else:
            return 0

    def average_words_per_sentence(self):
        if (len(self.get_number_of_words_in_sentences())) > 0 and self.get_number_of_sentences() > 0:
            return reduce(lambda x, y: x + y, self.get_number_of_words_in_sentences()) / float(
                self.get_number_of_sentences())
        else:
            return 0

    def get_number_of_sentences(self):
        if self.number_of_sentences == None:
            self.number_of_sentences = len(self.get_sentences())
        return self.number_of_sentences

    def check_if_url_present(self):
        if re.search(r'(https?://[^\s]+)', self.input_string) == None:
            return 0
        else:
            return 1

    def get_total_number_of_characters_in_words(self):
        if self.total_number_of_characters_in_words == None:
            result = 0
            words_in_sentences = self.get_words_in_sentences()
            for sentence in words_in_sentences:
                for word in sentence:
                    result = result + len(word)
            self.total_number_of_characters_in_words = result
        return self.total_number_of_characters_in_words

    def get_readability_score(self):
        if self.readability_score == 0 and self.get_total_words() > 0 and self.get_number_of_sentences() > 0:
            self.readability_score = 4.71 * (
                self.get_total_number_of_characters_in_words() / float(self.get_total_words())) + 0.5 * (
                self.get_total_words() / float(self.get_number_of_sentences())) - 21.43
        return self.readability_score

    def number_of_punctuation_marks(self):
        return len(re.findall("[,().;{}[\]<>\-?!]", self.input_string))

    def get_misspelled_words(self):
        if self.misspelled_words == None:
            result = []
            words_in_sentences = self.get_words_in_sentences()
            for sentence in words_in_sentences:
                for word in sentence:
                    if spell(word) != word:
                        result.append(word)
            self.misspelled_words = result
        return self.misspelled_words

    def number_of_misspelled_words(self):
        return len(self.get_misspelled_words())

    def grammar_checking(self):
        try:
            matches = TOOL.check(self.input_string)
            # return len(matches)
            if len(matches) == 0:
                return 1
            else:
                return 0
        except:
            return -1
