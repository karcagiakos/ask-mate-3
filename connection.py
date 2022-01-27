import csv
import time, datetime


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


def new_question(title, message, file_name):
    saved_data = {}
    questions = read_questions()
    last_id = sorted(questions, key=lambda x: int(x['id']), reverse=True)[0]['id']
    saved_data['id'] = int(last_id) + 1
    saved_data['submission_time'] = int(time.time())
    saved_data['view_number'] = 0
    saved_data['vote_number'] = 0
    saved_data['title'] = title
    saved_data['message'] = message
    if file_name == "":
        saved_data['image'] = 0
    else:
        saved_data['image'] = file_name
    questions.append(saved_data)
    write_questions(questions)

def new_answer(id, message, file_name):
    saved_data = {}
    answers = read_answers()
    last_id = sorted(answers, key=lambda x: int(x['id']), reverse=True)[0]['id']
    saved_data['id'] = int(last_id) + 1
    saved_data['submission_time'] = int(time.time())
    saved_data['vote_number'] = 0
    saved_data['question_id'] = id
    saved_data['message'] = message
    if file_name == "":
        saved_data['image'] = 0
    else:
        saved_data['image'] = file_name
    answers.append(saved_data)
    write_answer(answers)