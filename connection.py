import csv
import datetime

def read_questions():
    questions = sorted(list(csv.DictReader(open('sample_data/question.csv'))), key= lambda x: x['submission_time'], reverse = True)
    return questions

def read_answers():
    answers = list(csv.DictReader(open('sample_data/answer.csv')))
    return answers

def write_questions(data):
    with open('sample_data/question.csv', 'w') as file:
        fieldnames = ['id','submission_time','view_number','vote_number','title','message','image']
        writer = csv.DictWriter(file, fieldnames=fieldnames,)
        writer.writeheader()
        for dicts in data:
            writer.writerow(dicts)

def write_answer(data):
    with open('sample_data/answer.csv', 'w') as file:
        fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
        writer = csv.DictWriter(file, fieldnames=fieldnames,)
        writer.writeheader()
        for dicts in data:
            writer.writerow(dicts)


def delete_question(id):
    questions = read_questions()
    answers = read_answers()
    for dict in questions:
        if int(dict['id']) == int(id):
            questions.remove(dict)
            write_questions(questions)
    new_answers = []
    for dict in answers:
        if int(dict['question_id']) != int(id):
            new_answers.append(dict)
    write_answer(new_answers)

def delete_answer(answer_id):
    answers = read_answers()
    for dict in answers:
        if int(dict['id']) == int(answer_id):
            answers.remove(dict)
    write_answer(answers)
