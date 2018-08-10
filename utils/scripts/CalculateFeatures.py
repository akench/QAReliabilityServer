#uses python3.6 32 bit
import re
import csv
import nltk
from nltk import sent_tokenize, word_tokenize, sent_tokenize, pos_tag, ne_chunk
import math
from textblob import TextBlob

from nltk.corpus import stopwords
s=set(stopwords.words('english'))

header = ['Question', 'Average IDF', 'Entropy', 'Polarity', 'Subjectivity']

NUMBER_OF_QUESTIONS = 1000


def getalltokens():
    tokens = []
    with open('input.csv', encoding='ISO-8859-1') as csvfile:   #utf-8 encoding throws an error becasue the csv file has incompatible encodings with utf-8
        reader = csv.reader(csvfile)   
        for line in reader:
            for field in line:
                tokens+=word_tokenize(str(field.encode('ISO-8859-1','strict')).lower().replace("b'","").replace("'","").replace("?","").replace(".","").replace("!","").replace(",","").replace("<br />",""))
    return tokens


alltokens = getalltokens()


with open('input.csv', encoding='ISO-8859-1') as csvfile:  #utf-8 encoding throws an error becasue the csv file has incompatible encodings with utf-8
    with open('output.csv', 'w', newline='') as myfile:
        reader = csv.reader(csvfile)
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)  
        wr.writerow(header)
        for line in reader:
            for field in line:                    
                tokenized_sents = word_tokenize(str(field.encode('ISO-8859-1','strict')).lower().replace("b'","").replace("'","").replace("?","").replace(".","").replace("!","").replace(",","").replace("<br />",""))
                sum = 0
                i = 0       
                H = 0    
                p = 0  
                try:
                    text_blob = TextBlob(field)
                    polarity = text_blob.polarity
                    subjectivity = text_blob.subjectivity
                except Exception:
                    polarity = 0
                    subjectivity = 0
                for t in  tokenized_sents:
                    if (not t in s):   
                        i = i+1 
                        sum = sum + alltokens.count(t) 
                        p = alltokens.count(t)/len(alltokens)
                        H = H + -p*math.log(p)                        

                if (i > 0):
                    idf = str(-math.log(NUMBER_OF_QUESTIONS/(sum/i)))
                else:
                    idf = -9
                wr.writerow([str(field.encode('ISO-8859-1','strict')).lower().replace("b'","").replace("'","").replace("?","").replace(".","").replace("!","").replace(",","").replace("<br />",""), idf, H, polarity, subjectivity]) 
               
