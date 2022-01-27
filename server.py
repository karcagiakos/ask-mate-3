from flask import Flask, render_template, redirect, request, url_for
import connection
import datetime
import time

app = Flask(__name__)




@app.route("/", methods=['GET', 'POST'])
def main():
    data = connection.read_questions()
    if request.method == 'POST':
        ordering_by = request.form['headers']
        if ordering_by == 'view_number' or ordering_by == 'vote_number':
            data = sorted(data, key=lambda x: int(x[ordering_by]))
        # connection.write_questions(data)
        else:
            data = sorted(data, key=lambda x: x[ordering_by].capitalize())
        return render_template('main_page.html', data=data)
    return render_template('main_page.html', data=data)


@app.route("/list", methods=['GET', 'POST'])
def list_questions(sort_by='submission_time'):
    data = connection.read_questions()
    if request.method == 'POST':
        ordering_by = request.form['headers'][:-1]
        if request.form['headers'][-1] == '+':
            if ordering_by == 'view_number' or ordering_by == 'vote_number':
                data = sorted(data, key=lambda x: int(x[ordering_by]))
        # connection.write_questions(data)
            else:
                data = sorted(data, key=lambda x: x[ordering_by].capitalize())
        else:
            if ordering_by == 'view_number' or ordering_by == 'vote_number':
                data = sorted(data, key=lambda x: int(x[ordering_by]))[::-1]
            # connection.write_questions(data)
            else:
                data = sorted(data, key=lambda x: x[ordering_by].capitalize())[::-1]
        return render_template('main_page.html', data=data)
    return render_template('main_page.html', data=data)

@app.route("/questions/<int:id>", methods=['GET', 'DELETE', 'POST'])
def get_answers(id):
    questions = connection.read_questions()
    question = []
    answer = []
    answers = connection.read_answers()
    for dicts in questions:
        if int(dicts['id']) == int(id):
            question.append(dicts['title'])
            question.append((dicts['message']))
            dicts['view_number'] = int(dicts['view_number']) + 1
            connection.write_questions(questions)
    for dicts in answers:
        if int(dicts['question_id']) == int(id):
            answer.append(dicts)
    return render_template('display_questions.html', id=id,questions=questions, answers=answers, question=question, answer=answer)

@app.route("/questions/<int:id>/new-answer", methods=['GET', 'POST'])
def get_new_answers(id):
    saved_data = {}
    answers = connection.read_answers()
    last_id = sorted(answers, key=lambda x: int(x['id']), reverse=True)[0]['id']
    if request.method == 'POST':
        saved_data['id'] = int(last_id) + 1
        saved_data['submission_time'] = int(time.time())
        saved_data['vote_number'] = 0
        saved_data['question_id'] = id
        saved_data['message'] = request.form['answer']
        saved_data['image'] = 0
        answers.append(saved_data)
        connection.write_answer(answers)
        return redirect(url_for('get_answers', id=id))
    return render_template('new_answer.html', id=id)


@app.route("/add_question", methods=['GET', 'POST'])
def add_question():
    saved_data = {}
    questions = connection.read_questions()
    last_id = sorted(questions, key=lambda x: int(x['id']), reverse=True)[0]['id']
    if request.method == "POST":
        saved_data['id'] = int(last_id) + 1
        saved_data['submission_time'] = int(time.time())
        saved_data['view_number'] = 0
        saved_data['vote_number'] = 0
        saved_data['title'] = request.form['title']
        saved_data['message'] = request.form['message']
        saved_data['image'] = 0
        questions.append(saved_data)
        connection.write_questions(questions)
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
                if request.form['option'] == 'UP':
                    dict['vote_number'] = str(int(dict['vote_number'])+1)
                    connection.write_answer(answers)
                    return redirect(url_for('get_answers', id=question_id))
                elif request.form['option'] == 'DOWN':
                    dict['vote_number'] = str(int(dict['vote_number']) - 1)
                    connection.write_answer(answers)
                    return redirect(url_for('get_answers', id=question_id))
    return render_template('display_answer.html', answer_id=answer_id)


@app.route('/question/<question_id>/vote_up')
@app.route('/question/<question_id>/vote_down')
def vote_question():
    pass




if __name__ == "__main__":
    app.run(
        #host = "192.168.1.100",
        debug = True,
        port = 2000
    )