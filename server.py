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
def list_questions():
    data = data_manager.get_questions()
    return render_template('main_page.html', data=data)

@app.route("/questions/<int:id>", methods=['GET','POST'])
def list_answers(id):
    answers = data_manager.list_answers(id)
    question = data_manager.get_single_question(id)
    data_manager.update_view_number(id)
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
    answer_ids = [x['id'] for x in data_manager.list_answers(question_id)]
    data_manager.delete_comment(question_id)
    for i in answer_ids:
        data_manager.delete_comment(i)
    data_manager.delete_answer_with_question(question_id)
    data_manager.delete_question_tag(question_id)
    data_manager.delete_question(question_id)
    return redirect('/list')


@app.route('/answer/<int:answer_id>', methods=['GET', 'POST'])
def display_answer(answer_id):
    answers = data_manager.display_answer(answer_id)
    return render_template('display_answer.html', answer_id=answer_id, answer=answers )

@app.route('/answer/<int:answer_id>/delete ', methods=['GET', 'POST'])
def delete_answer(answer_id):
    answer_ids = [x['id'] for x in data_manager.list_answers(answer_id)]
    for i in answer_ids:
        data_manager.delete_comment(i)
    data_manager.delete_answer(answer_id)
    return redirect('/')


@app.route('/answer/<int:answer_id>/vote_up', methods=['GET', 'POST'])
def vote_up_answer(answer_id):
    question_id = data_manager.display_answer(answer_id)[0]['question_id']
    vote_up = request.args.get('vote_up')
    if vote_up:
        data_manager.update_answer_vote(answer_id, 1)
        return redirect(url_for('list_answers', id=question_id))
    return render_template('display_answer.html', answer_id=answer_id)



@app.route('/answer/<int:answer_id>/vote_down', methods=['GET', 'POST'])
def vote_down_answer(answer_id):
    question_id = data_manager.display_answer(answer_id)[0]['question_id']
    vote_down = request.args.get('vote_down')
    if vote_down:
        data_manager.update_answer_vote(answer_id, -1)
        return redirect(url_for('list_answers', id=question_id))
    return render_template('display_answer.html', answer_id=answer_id)




@app.route('/question/<int:question_id>/vote_up', methods=['GET', 'POST'])
def vote_up_question(question_id):
    vote_up = request.args.get('vote-up')
    answers = data_manager.list_answers(question_id)
    question = data_manager.get_single_question(question_id)
    if vote_up:
        data_manager.update_question_vote(question_id, 1)
        return redirect('/list')
    return render_template('display_questions.html', id=question_id, question=question, answer=answers)


@app.route('/question/<int:question_id>/vote_down', methods=['GET', 'POST'])
def vote_down_question(question_id):
    vote_down = request.args.get('vote-down')
    answers = data_manager.list_answers(question_id)
    question = data_manager.get_single_question(question_id)
    if vote_down:
        data_manager.update_question_vote(question_id, -1)
        return redirect('/list')
    return render_template('display_questions.html', id=question_id, question=question, answer=answers)






if __name__ == "__main__":
    app.run(
        #host = "192.168.1.100",
        debug = True,
        port = 2000
    )