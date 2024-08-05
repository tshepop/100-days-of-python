import json
from datetime import datetime
from smtplib import SMTP
import os
import config

from flask import Flask, redirect, render_template, request, url_for, flash


# data from npoint api
# url_addr = "https://api.npoint.io/8ac47f941e3696aa2619"
# r = requests.get(url=url_addr)
# print(f"Status: {r.status_code}")
# response = r.json()

# open a local json file for testing
with open("blog.json") as f:
    response = json.load(f)

YEAR = datetime.now().year
EMAIL_ACC = os.environ.get(config.EMAIL_ACC)
PASSWORD = os.environ.get(config.PASSWORD)
email_to = EMAIL_ACC


app = Flask(__name__)
app.secret_key = "Iloveme"


@app.route("/")
def index():

    return render_template("index.html",
                           year=YEAR,
                           posts=response)


@app.route("/post/<int:id>")
def post(id):
    all_posts = None

    for blog_post in response:
        if blog_post["id"] == id:
            all_posts = blog_post
            # image_name = str(blog_post['image']).split(".")[0]

    # year = datetime.now().year

    return render_template("post.html",
                           year=YEAR,
                           post=all_posts)


@app.route("/about")
def about():

    return render_template("about.html", year=YEAR)


@app.route("/contact", methods=("GET", "POST"))
def contact():
    message = "Thank you, your message was delivered!"

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        body = request.form["message"]
        error = None

        if not name or not email or not phone or not body:
            error = "All fields are required!"

        if error:
            flash(error)
            return redirect(url_for("contact"))
        else:

            try:
                with SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user=EMAIL_ACC, password=PASSWORD)
                    connection.sendmail(
                        from_addr=email,
                        to_addrs=email_to,
                        msg=f"Subject: test email\n\n{body}")
            except Exception as e:
                return e

            return render_template("subscribe.html",
                                   email_from=email,
                                   email_to=email_to,
                                   body=body,
                                   message=message,
                                   year=YEAR)

    return render_template("contact.html", year=YEAR)


@app.route("/email", methods=("GET", "POST"))
def email():
    heading = "Thank you, your message was delivered!"
    error = None

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        body = request.form.get("message")
        request.form.data

        if not name or not email or not phone or not body:
            error = "All the fields are required."
        elif not email:
            error = "The email address is required."
        elif not phone:
            error = "The phone number is required."
        elif not body:
            error = "Message is required."

        if error:
            flash(error)
            return redirect(url_for("contact"))

    return render_template("subscribe.html",
                           heading=heading,
                           name=name,
                           email=email,
                           phone=phone,
                           message=body)


if __name__ == "__main__":
    app.run()
