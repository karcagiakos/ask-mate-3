from flask import Flask, render_template, redirect, request
import connection



app = Flask(__name__)

@app.route("/")
def main():
    return render_template('main_page.html', data=connection.read_questions())


@app.route("/list")
def list_questions():
    return render_template('main_page.html', data=connection.read_questions())

#@app.route("/questions/<int: id>")
#def get_answers():
  #  pass
 #   return


@app.route("/add_question", methods=['GET', 'POST'])
def add_question():
    return render_template('add_question.html')


if __name__ == "__main__":
    app.run(
        debug = True,
        port = 2000
    )
