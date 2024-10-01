from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_ckeditor.utils import cleanify
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_required, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
# Import your forms from the forms.py
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
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
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['CKEDITOR_SERVE_LOCAL'] = True
ckeditor = CKEditor(app)
Bootstrap5(app)


# TODO: Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


# TODO: Create a User table for all your registered users.
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    post: Mapped[list["BlogPost"]] = relationship(back_populates="author")
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="comment_author")


class Comment(db.Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    comment_author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    comment_author: Mapped[list["User"]] = relationship(
        back_populates="comments")
    comment_blog_post: Mapped[list["BlogPost"]] = relationship(
        back_populates="comments")
    comment_post_id: Mapped[int] = mapped_column(ForeignKey("blog_posts.id"))


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, ident=user_id)


def admin_only(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not current_user.id == 1:
            return abort(403)
        return function(*args, **kwargs)
    return decorated_function


# TODO: Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        error = None

        user = db.session.execute(
            db.select(User).where(User.email == email)).scalar()

        if user:
            error = "You've already signed up with that email, Please log in!"

        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(
                password=password, method="pbkdf2:sha256", salt_length=12)
        )
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            print(e)
            flash(error)
            return redirect(url_for("login"))
        else:
            login_user(new_user)
            return redirect(url_for("get_all_posts"))

    return render_template("register.html", form=form)


# TODO: Retrieve a user from the database based on their email.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("get_all_posts"))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = db.session.execute(
            db.select(User).where(User.email == email)).scalar()

        if not user:
            flash("The email does not exist! Try again.")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            flash("The password is invalid! Try again.")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("get_all_posts"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


# TODO: Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def show_post(post_id):

    form = CommentForm()
    requested_post = db.get_or_404(BlogPost, post_id)

    if form.validate_on_submit():
        error = None

        if current_user.is_authenticated:

            try:
                new_comment = Comment(
                    text=cleanify(form.text.data),
                    comment_author=current_user,
                    comment_blog_post=requested_post
                )
            except Exception:
                error = "Problem saving your comment."
                flash(error)
            else:
                db.session.add(new_comment)
                db.session.commit()
                form.text.data = ""
        else:
            error = "You have to login to comment."
            flash(error)
            return redirect(url_for("login"))

    return render_template("post.html", post=requested_post,
                           form=form)


# TODO: Use a decorator so only an admin user can create a new post
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


# TODO: Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


# TODO: Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
