from flask import Flask, flash, render_template, redirect, request, url_for, session, escape
from bonus_questions import SAMPLE_QUESTIONS
import datetime
from werkzeug.utils import secure_filename
import os
import data_manager

ALLOWED_EXTENSIONS = {'png', 'jpg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/static/images'
app.secret_key = b'_5#y2L"F4Q8z\xec]/'

@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


@app.route("/", methods=['GET'])
def show_main_page():
    username = 'stranger'
    if 'username' in session:
        username = escape(session['username'])
    order_by = request.args.get('headers')
    sort = request.args.get('order')
    data = data_manager.last_five_questions(order_by='submission_time')
    if order_by and sort:
        if sort == 'DESC':
            data = data_manager.last_five_questions(order_by)[::-1]
        else:
            data = data_manager.last_five_questions(order_by)
    return render_template('main_page.html', data=data, username=username)


@app.route("/list", methods=['GET', 'POST'])
def list_questions():
    username = 'stranger'
    if 'username' in session:
        username = escape(session['username'])
    data = data_manager.get_questions()
    order_by = request.args.get('headers')
    sort = request.args.get('order')
    if order_by and sort:
        if sort == 'DESC':
            data = data_manager.sort_questions(order_by)[::-1]
        else:
            data = data_manager.sort_questions(order_by)
    return render_template('main_page.html', data=data, username=username)


@app.route("/questions/<int:id>", methods=['GET','POST'])
def list_answers(id):
    # tags = [x['name'] for x in data_manager.get_question_id_with_tag_name(id)]
    username = 'stranger'
    if 'username' in session:
        username = escape(session['username'])
    tags = data_manager.get_question_id_with_tag_name(id)
    answers = data_manager.list_answers(id)
    question = data_manager.get_single_question(id)
    answer_comments = data_manager.get_all_the_comments()
    comments = data_manager.get_comments_for_questions(id)
    answer_ids = [x['id'] for x in answers]
    comment_ids = set([x['answer_id'] for x in answer_comments])
    data_manager.update_view_number(id)

    return render_template('display_questions.html', comment_ids=comment_ids, question_id=id, id=id, question=question, answer=answers, comments=comments, tags=tags, answer_comments=answer_comments, answer_ids=answer_ids, username=username)


@app.route("/questions/<int:id>/new-answer", methods=['GET', 'POST'])
def add_new_answer(id):
    if 'username' in session:
        if request.method == 'POST':
            temp_file_name = request.files['file']
            file_name = str(request.files['file']).split()[1][1:-1]
            if temp_file_name:
                temp_file_name.save(os.path.join('static/images/', temp_file_name.filename))
            data = [str(datetime.datetime.now()),0,id,request.form['answer'],file_name]
            data_manager.add_new_answer(data)
            return redirect(url_for('list_answers', id=id))
        return render_template('new_answer.html', id=id)
    else:
        return redirect(url_for('list_answers', id=id))


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if 'username' in session:
        if request.method == "POST":
            temp_file_name = request.files['file']
            file_name = str(request.files['file']).split()[1][1:-1]
            if temp_file_name:
                temp_file_name.save(os.path.join('static/images/', temp_file_name.filename))
            data = [str(datetime.datetime.now()), 0, 0, request.form['title'], request.form['message'], file_name]
            data_manager.add_new_question(data)
            return redirect('/list')
        return render_template('add_question.html')
    else:
        return redirect('/')


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
    data_manager.delete_question(question_id)
    return redirect('/list')


@app.route('/answer/<int:answer_id>/delete ', methods=['GET', 'POST'])
def delete_answer(answer_id):
    question_id = data_manager.display_answer(answer_id)[0]['question_id']
    data_manager.delete_answer(answer_id)
    return redirect(url_for('list_answers', id=question_id))


@app.route('/answer/<int:answer_id>/vote_up', methods=['GET', 'POST'])
def vote_up_answer(answer_id):
    question_id = data_manager.display_answer(answer_id)[0]['question_id']
    vote_up = request.args.get('vote_up')
    if vote_up:
        data_manager.update_answer_vote(answer_id, 1)
        return redirect(url_for('list_answers', id=question_id))


@app.route('/answer/<int:answer_id>/vote_down', methods=['GET', 'POST'])
def vote_down_answer(answer_id):
    question_id = data_manager.display_answer(answer_id)[0]['question_id']
    vote_down = request.args.get('vote_down')
    if vote_down:
        data_manager.update_answer_vote(answer_id, -1)
        return redirect(url_for('list_answers', id=question_id))


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


@app.route('/question/<int:question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == 'POST':
        data = [question_id,request.form['comment'],str(datetime.datetime.now()),0]
        data_manager.add_new_comment_question(data)
        return redirect(url_for('list_answers', id=question_id))
    return render_template('add_new_comment.html', id=question_id)


@app.route('/answer/<int:answer_id>/new-comment', methods=['GET','POST'])
def add_comment_to_answer(answer_id):
    question_id = data_manager.display_answer(answer_id)[0]['question_id']
    if request.method == 'POST':
        data = [answer_id,request.form['comment'], str(datetime.datetime.now()),0]
        data_manager.add_new_comment_answer(data)
        return redirect(url_for('list_answers', id=question_id))
    return render_template('add_new_comment_for_answers.html', answer_id=answer_id, question_id=question_id)


@app.route('/search')
def search_questions():
    searched_question = request.args.get("q")
    if searched_question:
        answers = data_manager.search_answers(searched_question)
        question_ids = set(x['question_id'] for x in data_manager.search_answers(searched_question))
        answer_ids = [x['id'] for x in answers]
        details = data_manager.search_questions(searched_question)
        details_ids = [x['id'] for x in details]
        for id in question_ids:
            if id not in details_ids:
                details.append(data_manager.get_single_question(id)[0])
        data_manager.markup(searched_question,details)
        data_manager.markup(searched_question,answers)
        ids_we_need = [x['id'] for x in details]
    else:
        return redirect('/')
    return render_template('searched_question.html', answer_ids=answer_ids, question_ids=question_ids, details=details, answers=answers, details_ids=ids_we_need)


@app.route('/answer/<int:answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    answers = data_manager.display_answer(answer_id)
    comments = data_manager.get_comments_for_answers(answer_id)
    if request.method == 'POST':
        data_manager.update_answer(answer_id,request.form['message'])
        return redirect(url_for('list_answers', id=answers[0]['question_id']))
    return render_template('edit_answer.html', answer_id=answer_id, answer=answers, comments=comments )


@app.route('/comment/<int:comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    comment = data_manager.get_comment(comment_id)
    question_id = comment[0]['question_id']
    answer_id = comment[0]['answer_id']
    if request.method == 'POST':
        data = [request.form['comment'], str(datetime.datetime.now()), comment[0]['id']]
        data_manager.update_comment(data)
        if not question_id:
            question_id = data_manager.get_question_id_by_answer_id(answer_id)[0]['question_id']
        return redirect(url_for('list_answers', id=question_id))
    return render_template('edit_comment.html', comment_id=comment_id, comment=comment)


@app.route('/comments/<int:comment_id>/delete', methods=['GET', 'POST'])
def delete_comment(comment_id):
    comment = data_manager.get_comment(comment_id)
    question_id = comment[0]['question_id']
    answer_id = comment[0]['answer_id']
    data_manager.delete_comment(comment_id)
    if not question_id:
        question_id = data_manager.get_question_id_by_answer_id(answer_id)[0]['question_id']
    return redirect(url_for('list_answers', id=question_id))


@app.route('/question/<int:question_id>/new-tag', methods = ['GET', 'POST'])
def new_tag(question_id):
    names = [x['name'] for x in data_manager.get_tag()]
    tags = data_manager.get_tag()
    if request.method == 'POST':
        if request.form['tag'] not in names:
            tag = request.form['tag']
            data_manager.add_tag(tag)
        tag_id = [x['id'] for x in data_manager.get_tag() if x['name'] == request.form['tag']]
        data_manager.add_tag_question([question_id, tag_id[0]])
    return render_template('new_tag.html', question_id=question_id, tags=tags)


@app.route('/question/<int:question_id>/tag/<int:tag_id>/delete')
def delete_tag(question_id,tag_id):
    ids = [question_id, tag_id]
    data_manager.delete_tag_from_question(ids)
    return redirect(url_for('list_answers', id=question_id))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    mails = [x['email'] for x in data_manager.get_emails_and_passwords()]
    if request.method == 'POST':
        if request.form['email'] not in mails:
            email = request.form['email']
            password = data_manager.hash_password(request.form['password'])
            reg_date = str(datetime.datetime.now())
            data_manager.add_new_user([email,password,reg_date,0,0,0,0])

            return redirect('/')
        else:
            flash("E-mail taken")
    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    users = [x['email'] for x in data_manager.get_emails_and_passwords()]
    if request.method == 'POST':
        if request.form['email'] in users:
            password = data_manager.get_password(request.form['email'])[0]['password_hash']
            if data_manager.verify_password(request.form['password'], password):
                session['username'] = request.form['email']
                return redirect(url_for('show_main_page'))
            else:
                return 'Invalid login attempt'
        else:
            return 'Invalid login attempt'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('show_main_page'))


if __name__ == "__main__":
    app.run(
        #host = "192.168.1.100",
        debug = True,
        port = 2000)