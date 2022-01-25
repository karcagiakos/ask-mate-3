from flask import Flask, render_template, redirect, request
import connection
import datetime
import time

app = Flask(__name__)



@app.route("/")
def main():
    return render_template('main_page.html', data=connection.read_questions())


@app.route("/list")
def list_questions():
    return render_template('main_page.html', data=connection.read_questions())

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
    return render_template('index.html', id=id, questions=questions, answers=answers, question=question, answer=answer)



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
        print(saved_data)
        questions.append(saved_data)
        print(questions)
        connection.write_questions(questions)
        return redirect('/list')
    return render_template('add_question.html')


if __name__ == "__main__":
    app.run(
        host = "192.168.1.100",
        debug = True,
        port = 2000
    )
