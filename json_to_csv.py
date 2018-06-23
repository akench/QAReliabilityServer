import json
import csv
import os, glob
from pprint import pprint

# URL    Question     Subject     Answer    Ratings    Thanks   
def get_relevant_csv_data(full_body):
    brainly_data = full_body['brainly_data']

    answer_list = []
    for obj in brainly_data['all_answers']:
        obj['href'] = full_body['href']
        obj['question_timestamp'] = brainly_data['date']
        answer_list.append(obj)

    return answer_list

# question,subject,text,rating,reputation,num_upvotes,num_thanks,href,question_timestamp
def write_all_objects_csv(writer, all_answers):
    print(all_answers)
    for obj in all_answers:
        print('writing')
        writer.writerow([obj['question'],
                         obj['subject'],
                         obj['text'],
                         obj['rating'],
                         obj['reputation'],
                         obj['num_upvotes'],
                         obj['num_thanks'],
                         obj['href'],
                         obj['question_timestamp']])

def main():
    os.chdir('./collection')
    json_list_for_csv = []
    for filename in glob.glob('*.json'):
        with open(filename, 'r') as json_file:
            full_body = json.load(json_file)
            for answer in get_relevant_csv_data(full_body):
                json_list_for_csv.append(answer)

    os.chdir('../')
    with open('test.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(json_list_for_csv[0])
        write_all_objects_csv(writer, json_list_for_csv)


if __name__ == "__main__":
    main()
