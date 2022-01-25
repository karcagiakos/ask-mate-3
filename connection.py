import csv


def read_questions():
    questions = sorted(list(csv.DictReader(open('sample_data/question.csv'))), key= lambda x: x['submission_time'], reverse = True)
    return questions

def read_answers():
    answers = list(csv.DictReader(open('sample_data/answer.csv')))
    return answers
