from flask import Flask, flash, render_template, redirect, request, url_for
import connection
import datetime
import jinja2
from werkzeug.utils import secure_filename
import os

import data_manager

ALLOWED_EXTENSIONS = {'png', 'jpg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/static/images'
env = jinja2.Environment()

# @app.template_filter('datetimeformat')
def datetime_format(value, format='%Y/%m/%d %H:%M:%S'):
    return value.strftime(format)



env.filters['datetime_format'] = datetime_format

@app.route("/", methods=['GET'])
def show_main_page():
    return redirect("/list")

@app.route("/list", methods=['GET', 'POST'])
def list_questions(sort_by='submission_time'):
    data = data_manager.get_questions()
    print(data)
    return render_template('main_page.html', data=data)

@app.route("/questions/<int:id>", methods=['GET','POST'])
def get_answers(id):
    answers = data_manager.display_answer(id)
    question = data_manager.get_single_question(id)
    # questions = data_manager.get_questions()
    # answers = data_manager.get_answers()
    # question = []
    # answer = []
    # for dicts in questions:
    #     if int(dicts['id']) == int(id):
    #         question.append(dicts['title'])
    #         question.append((dicts['message']))
    #         dicts['view_number'] = int(dicts['view_number']) + 1
    #         connection.write_questions(questions)
    # for dicts in answers:
    #     if int(dicts['question_id']) == int(id):
    #         answer.append(dicts)
    return render_template('display_questions.html', id=id,
                           question=question, answer=answers)

@app.route("/questions/<int:id>/new-answer", methods=['GET', 'POST'])
def get_new_answers(id):
    if request.method == 'POST':
        questions = connection.read_questions()
        file_name = request.files['file']
        file_name1 = str(request.files['file']).split()[1][1:-1]
        if file_name:
            file_name.save(os.path.join('static/images/', file_name.filename))
        connection.new_answer(id, request.form['answer'], file_name1)
        return redirect(url_for('get_answers', id=id))
    return render_template('new_answer.html', id=id)


@app.route("/add_question", methods=['GET', 'POST'])
def add_question():
    if request.method == "POST":
        file_name = request.files['file']
        file_name1 = str(request.files['file']).split()[1][1:-1]
        if file_name:
            file_name.save(os.path.join('static/images/', file_name.filename))
        connection.new_question(request.form['title'], request.form['message'], file_name1)
        return redirect('/list')
    return render_template('add_question.html')

@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    questions = connection.read_questions()
    title = []
    message = []
    for dict in questions:
        if int(dict['id']) == int(question_id):
            title.append(dict['title'])
            message.append(dict['message'])
    if request.method == 'POST':
        for dict in questions:
            if int(dict['id']) == int(question_id):
                dict['title'] = request.form['title']
                dict['message'] = request.form['message']
                connection.write_questions(questions)
                return redirect(url_for('get_answers', id=question_id))

    return render_template('edit_question.html', question_id=question_id, title=title, message=message)



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