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


# def info():
#     image_dict = {
#         "91magazine": "https://unsplash.com/photos/brown-and-black-camera-E_s7-xq0FAk?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash",
#         "adamsmigielski": "https://unsplash.com/photos/a-person-holding-a-cell-phone-in-front-of-a-stock-chart-K5mPtONmpHM?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash",
#         "robertocortese": "https://unsplash.com/photos/silver-iphone-6-on-white-table-F1I4IN86NiE?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash",
#         "glencarrie": "https://unsplash.com/photos/a-computer-screen-with-a-bunch-of-lines-on-it-mQ8GR35n8QQ?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash",
#         "nasahubblespacetelescope": "https://unsplash.com/photos/a-very-large-star-cluster-in-the-sky-gZN4couQZx0?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash",
#         "anniespratt": "https://unsplash.com/photos/plant-near-organizer-and-tablet-keyboard-ase-bGdiuIyN3Rs?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash"
#     }


app = Flask(__name__)


@app.route("/")
def index():
    year = datetime.now().year
    return render_template("index.html",
                           year=year,
                           posts=response)


@app.route("/post/<int:id>")
def post(id):
    all_posts = None

    for blog_post in response:
        if blog_post["id"] == id:
            all_posts = blog_post
            # image_name = str(blog_post['image']).split(".")[0]

    year = datetime.now().year

    return render_template("post.html",
                           year=year,
                           post=all_posts)


if __name__ == "__main__":
    app.run()
