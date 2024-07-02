import random
from flask import Flask, render_template

app = Flask(__name__)

rand_num = random.randint(1, 10)
# print(rand_num)


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/guess/<int:number>")
def guesses(number):

    if number < rand_num:
        message = "Your guess is low"

        return render_template("low.html", message=message, number=number)

    elif number > rand_num:
        message = "Your guess is high"

        return render_template("high.html", message=message, number=number)

    elif number == rand_num:
        message = "Correct Guess"

        return render_template("correct_guess.html",
                               message=message,
                               number=number)


@app.errorhandler(404)
def page_not_found(e):
    err_msg = "<h1>404</h1>"
    message = "<h2>Oops there is nothing here!</h2>"
    return f"{ err_msg }\n{ message }", 404


if __name__ == "__name__":
    app.run()
