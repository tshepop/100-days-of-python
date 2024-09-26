from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# config login manager
login_manager = LoginManager()
login_manager.init_app(app)


# CREATE TABLE IN DB
class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))


@app.route('/')
def home():
    logged_in_message = "You are already logged in"
    return render_template("index.html", message=logged_in_message)


@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        error = None

        user = db.session.execute(
            db.select(User).where(User.email == email)).scalar()

        if user:
            error = "You've already signed up with that email, Please log in!"

        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(
                password, method='pbkdf2:sha256', salt_length=8)
        )

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception:
            flash(error)
            return redirect(url_for("login"))
        else:
            login_user(new_user)
            return redirect(url_for("secrets"))

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = db.session.execute(
            db.select(User).where(User.email == email)).scalar()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("secrets"))
        else:
            flash("Invalid email or password")
            return redirect(url_for("login"))

    # user_email = request.form.get("email")
    # user_pass = request.form.get("password")

    # user = db.session.execute(db.select(User).where(
    #     User.email == user_email)).scalar()
    # print(user.id)

    # login_user(user)

    # print("Logged in Successfully.")

    # if request.method == "POST":
    #     user_email = request.form.get('email')
    #     user_pass = request.form.get('password')
    #     error = None
    #     print(user_email)

    #     user = db.session.execute(
    #         db.select(User).filter_by(email=user_email)).scalars().first()

    #     if user is None:
    #         error = "Incorrect email"
    #         print(error)
    #     elif not check_password_hash(user.password, user_pass):
    #         error = "Incorrect password"
    #         print(error)

    #     if error is None:
    #         print("Welcome to home.")
    #     # flash(error)

    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():

    if current_user.is_authenticated:
        user = current_user.name

    return render_template("secrets.html", name=user)


@app.route('/logout')
@login_required
def logout():

    logout_user()
    return redirect(url_for("home"))


@app.route('/download')
@login_required
def download():

    # return send_from_directory(directory="static", path="files/cheat_sheet.pdf", max_age=0)
    return send_from_directory(directory=app.static_folder,
                               path="files/cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)
