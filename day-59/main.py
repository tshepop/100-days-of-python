import json
from datetime import datetime
from flask import Flask, render_template


# data from npoint api
# url_addr = "https://api.npoint.io/8ac47f941e3696aa2619"
# r = requests.get(url=url_addr)
# print(f"Status: {r.status_code}")
# response = r.json()

# open a local json file for testing
with open("blog.json") as f:
    response = json.load(f)

YEAR = datetime.now().year

app = Flask(__name__)


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


@app.route("/contact")
def contact():
    return render_template("contact.html", year=YEAR)


if __name__ == "__main__":
    app.run()
