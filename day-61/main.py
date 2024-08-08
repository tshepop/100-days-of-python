from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField
from wtforms.validators import Email, Length, InputRequired

from flask_bootstrap import Bootstrap4
import config


class MyForm(FlaskForm):
    email = EmailField(label="Email", validators=[InputRequired(), Email()])
    password = PasswordField(label="Password", validators=[InputRequired(),
                             Length(min=8, max=12)])
    submit = SubmitField(label="Log In")


app = Flask(__name__)
app.secret_key = config.SECRET_KEY

Bootstrap4(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/denied")
def denied():
    return render_template("denied.html")


@app.route("/login", methods=("GET", "POST"))
def login():
    form = MyForm()
    if form.validate_on_submit():
        admin = "admin@email.com"
        print(form.email.data)
        if form.email.data != admin:
            return redirect(url_for("denied"))
        else:
            return redirect(url_for("success"))

    return render_template("login.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
