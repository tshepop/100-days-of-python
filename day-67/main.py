from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime
import config

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = config.APP_SECRET
Bootstrap5(app)

# CREATE DATABASE


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


class AddBlogPost(FlaskForm):
    title = StringField(label='Blog Post Title', validators=[DataRequired()])
    subtitle = StringField(label='Subtitle', validators=[DataRequired()])
    author = StringField(label='Your Name', validators=[DataRequired()])
    img_url = URLField(label='Blog Image URL', validators=[URL()])
    body = CKEditorField('Blog Content')
    submit = SubmitField(label='SUBMIT POST')


@app.route('/')
def get_all_posts():

    posts = db.session.execute(db.select(BlogPost)).scalars().all()

    return render_template("index.html", all_posts=posts)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):

    requested_post = db.get_or_404(BlogPost, ident=post_id)
    return render_template("post.html", post=requested_post)


@app.route('/new-post', methods=['GET', 'POST'])
def add_post():
    form = AddBlogPost()

    blog_post_date = datetime.now().strftime("%B %d, %Y")
    if form.validate_on_submit():

        new_blog_post = BlogPost(
            title=request.form.get('title'),
            subtitle=request.form.get('subtitle'),
            date=blog_post_date,
            author=request.form.get('author'),
            img_url=request.form.get('img_url'),
            body=cleanify(request.form.get('body'))
        )

        db.session.add(new_blog_post)
        db.session.commit()

        return redirect(url_for('get_all_posts'))

    return render_template("make-post.html", form=form)


@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    # form = AddBlogPost()
    edit_post = db.get_or_404(BlogPost, ident=post_id)

    # populate the form fields with data from db
    edit_form = AddBlogPost(
        title=edit_post.title,
        subtitle=edit_post.subtitle,
        author=edit_post.author,
        img_url=edit_post.img_url,
        body=edit_post.body
    )
    # retrieve data from the form fields and pass to db object
    if request.method == 'POST':
        edit_post.title = edit_form.title.data
        edit_post.subtitle = edit_form.subtitle.data
        edit_post.author = edit_form.author.data
        edit_post.img_url = edit_form.img_url.data
        edit_post.body = cleanify(edit_form.body.data)

        db.session.commit()

        return redirect(url_for('show_post', post_id=edit_post.id))

    return render_template('make-post.html',
                           form=edit_form,
                           edit_post=edit_post)

# TODO: delete_post() to remove a blog post from the database

# Below is the code from previous lessons. No changes needed.


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
