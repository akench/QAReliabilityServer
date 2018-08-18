#uses python3.6 32 bit
import csv
import math
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk import word_tokenize

STOPWORDS = set(stopwords.words('english'))
HEADER = ['Question', 'Average IDF', 'Entropy', 'Polarity', 'Subjectivity']
NUMBER_OF_QUESTIONS = 1000

def strip_field(text):
    return str(text.encode('ISO-8859-1', 'strict'))     \
                .lower()                                \
                .replace("b'", "")                      \
                .replace("'", "")                       \
                .replace("?", "")                       \
                .replace(".", "")                       \
                .replace("!", "")                       \
                .replace(",", "")                       \
                .replace("<br />", "")

def get_all_tokens(text):
    text = strip_field(text)
    return word_tokenize(text)

def get_all_tokens_from_file():
    tokens = []
    #utf-8 encoding throws an error becasue the csv file has incompatible encodings with utf-8
    with open('input.csv', encoding='ISO-8859-1') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            for field in line:
                tokens += get_all_tokens(field)
    return tokens

def get_polarity_subjectivity(text):
    try:
        text_blob = TextBlob(text)
        polarity = text_blob.polarity
        subjectivity = text_blob.subjectivity
        return polarity, subjectivity
    except Exception:
        return 0, 0

def get_all_scores(text, num_questions=1, all_tokens=None):
    if not all_tokens:
        all_tokens = get_all_tokens(text)

    text = strip_field(text)
    tokenized_sents = word_tokenize(text)
    polarity, subjectivity = get_polarity_subjectivity(text)

    sum = 0
    i = 0
    H = 0
    p = 0

    for t in  tokenized_sents:
        if t in STOPWORDS:
            continue

        i = i+1
        sum = sum + all_tokens.count(t)
        p = all_tokens.count(t)/len(all_tokens)
        H = H + -p*math.log(p)

    if i > 0:
        idf = str(-math.log(num_questions/(sum/i)))
    else:
        idf = -9

    return text, idf, H, polarity, subjectivity

if __name__ == "__main__":
    All_TOKENS = get_all_tokens_from_file()

    #utf-8 encoding throws an error becasue the csv file has incompatible encodings with utf-8
    with open('input.csv', encoding='ISO-8859-1') as csvfile:
        with open('output.csv', 'w', newline='') as myfile:
            READER = csv.reader(csvfile)
            WRITER = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            WRITER.writerow(HEADER)
            for line in READER:
                for field in line:
                    text, idf, H, polarity, subjectivity = get_all_scores(field, num_questions=NUMBER_OF_QUESTIONS, all_tokens=All_TOKENS)
                    WRITER.writerow([text, idf, H, polarity, subjectivity])
