from flask import Flask, render_template, redirect, request, url_for
import connection
import datetime
import time

app = Flask(__name__)



@app.route("/", methods=['GET', 'POST'])
def main():
    data = connection.read_questions()
    if request.method == 'POST':
        data = sorted(data, key=lambda x: x[request.form[options['name']]])
        connection.write_questions(data)
        return redirect('/list')
    return render_template('main_page.html', data=data)


@app.route("/list", methods=['GET', 'POST'])
def list_questions(sort_by='submission_time'):
    data = connection.read_questions()
    if request.method == 'POST':
        ordering_by = request.form['headers']

        # data = sorted(data, key=lambda x: x[request.form[option['name']]])
        # connection.write_questions(data)
        return redirect('/list')
    return render_template('main_page.html', data=data)

@app.route("/questions/<int:id>")
def get_answers(id):
    questions = connection.read_questions()
    question = []
    answer = []
    answers = connection.read_answers()
    for dicts in questions:
        if int(dicts['id']) == int(id):
           question.append(dicts['title'])
           question.append((dicts['message']))
    for dicts in answers:
        if int(dicts['question_id']) == int(id):
            answer.append(dicts)
    return render_template('display_questions.html', id=id, questions=questions, answers=answers, question=question, answer=answer)

@app.route("/questions/<int:id>/new-answer", methods=['GET', 'POST'])
def get_new_answers(id):
    saved_data = {}
    answers = connection.read_answers()
    if request.method == 'POST':
        # x = request.form.to_dict()
        # print(x)
        # return redirect(url_for('get_answers')
        saved_data['id'] = len(answers) + 1
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
    if request.method == "POST":
        saved_data['id'] = len(questions) + 1
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


if __name__ == "__main__":
    app.run(
        #host = "192.168.1.100",
        debug = True,
        port = 2000
    )
