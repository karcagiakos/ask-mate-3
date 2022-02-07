from flask import Flask, flash, render_template, redirect, request, url_for
import connection
import datetime
from werkzeug.utils import secure_filename
import os

import data_manager

ALLOWED_EXTENSIONS = {'png', 'jpg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/static/images'


@app.route("/", methods=['GET'])
def show_main_page():
    return redirect("/list")

@app.route("/list", methods=['GET', 'POST'])
def list_questions(sort_by='submission_time'):
    data = data_manager.get_questions()
    return render_template('main_page.html', data=data)

@app.route("/questions/<int:id>", methods=['GET','POST'])
def list_answers(id):
    answers = data_manager.display_answer(id)
    question = data_manager.get_single_question(id)
    return render_template('display_questions.html', id=id, question=question, answer=answers)

@app.route("/questions/<int:id>/new-answer", methods=['GET', 'POST'])
def add_new_answer(id):
    if request.method == 'POST':
        temp_file_name = request.files['file']
        file_name = str(request.files['file']).split()[1][1:-1]
        if temp_file_name:
            temp_file_name.save(os.path.join('static/images/', temp_file_name.filename))
        data = [str(datetime.datetime.now()),0,id,request.form['answer'],file_name]
        data_manager.add_new_answer(data)
        return redirect(url_for('list_answers', id=id))
    return render_template('new_answer.html', id=id)


@app.route("/add_question", methods=['GET', 'POST'])
def add_question():
    if request.method == "POST":
        temp_file_name = request.files['file']
        file_name = str(request.files['file']).split()[1][1:-1]
        if temp_file_name:
            temp_file_name.save(os.path.join('static/images/', temp_file_name.filename))
        data = [str(datetime.datetime.now()), 0, 0, request.form['title'], request.form['message'], file_name]
        data_manager.add_new_question(data)
        return redirect('/list')
    return render_template('add_question.html')

@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question = data_manager.get_single_question(question_id)
    if request.method == 'POST':
        data = [request.form['title'], request.form['message'],question_id]
        data_manager.update_question(data)
        return redirect(url_for('list_answers', id=question_id))

    return render_template('edit_question.html', question_id=question_id, question=question)



@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    connection.delete_question(question_id)
    return redirect('/list')


@app.route('/answer/<int:answer_id>', methods=['GET', 'POST'])
def display_answer(answer_id):
    answers = connection.read_answers()
    answer = ''
    for dict in answers:
        if int(dict['id']) == int(answer_id):
            answer += dict['message']
    return render_template('display_answer.html', answer_id=answer_id, answer=answer )

@app.route('/answer/<answer_id>/delete ', methods=['GET', 'POST'])
def delete_answer(answer_id):
    connection.delete_answer(answer_id)
    return redirect('/')


@app.route('/answer/<answer_id>/vote_down', methods=['GET', 'POST'])
@app.route('/answer/<answer_id>/vote_up', methods=['GET', 'POST'])
def vote_answer(answer_id):
    question_id = ''
    answers = connection.read_answers()
    if request.method == 'POST':
        for dict in answers:
            if dict['id'] == answer_id:
                question_id += dict['question_id']
                if request.form['option'] == 'UPVOTE':
                    dict['vote_number'] = str(int(dict['vote_number'])+1)
                    connection.write_answer(answers)
                    return redirect(url_for('get_answers', id=question_id))
                elif request.form['option'] == 'DOWNVOTE' \
                                               '':
                    dict['vote_number'] = str(int(dict['vote_number']) - 1)
                    connection.write_answer(answers)
                    return redirect(url_for('get_answers', id=question_id))
    return render_template('display_answer.html', answer_id=answer_id)


@app.route('/question/<question_id>/vote_up', methods=['GET', 'POST'])
@app.route('/question/<question_id>/vote_down', methods=['GET', 'POST'])
def vote_question(question_id):
    questions = connection.read_questions()
    if request.method == 'POST':
        for dict in questions:
            if dict['id'] == question_id:
                if request.form['option'] == 'UPVOTE':
                    dict['vote_number'] = int(dict['vote_number']) + 1
                    connection.write_questions(questions)
                    return redirect('/list')
                elif request.form['option'] == 'DOWNVOTE':
                    dict['vote_number'] = int(dict['vote_number']) - 1
                    connection.write_questions(questions)
                    return redirect('/list')
    return render_template('display_question.html', question_id=question_id)





if __name__ == "__main__":
    app.run(
        #host = "192.168.1.100",
        debug = True,
        port = 2000
    )