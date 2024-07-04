# import json
from flask import Flask, render_template
import requests

# location of the npoint bin:
# https://www.npoint.io/docs/8ac47f941e3696aa2619

# open a local json file for testing
# with open("blog.json") as f:
#     response = json.load(f)

# data from npoint api
url_addr = "https://api.npoint.io/8ac47f941e3696aa2619"
r = requests.get(url=url_addr)
print(f"Status: {r.status_code}")
response = r.json()

app = Flask(__name__)


@app.route('/')
def home():
    # url = "https://api.npoint.io/8ac47f941e3696aa2619"
    # r = requests.get(url=url)
    # response = r.json()

    return render_template("index.html", all_posts=response)


@app.route("/post/<int:id>")
def post(id):
    # fake blog posts url
    request_post = None
    for blog_post in response:
        if blog_post["id"] == id:
            request_post = blog_post
    return render_template("post.html", post=request_post)


if __name__ == "__main__":
    app.run()
