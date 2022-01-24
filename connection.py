import csv


def read_questions():
    data = list(csv.DictReader(open('sample_data/question.csv')))
    return data


