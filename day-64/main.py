import datetime

from flask import Flask, render_template, redirect, session, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

import config

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"

# TMDB api key

HEADERS = {
    "accept": "application/json",
    "Authorization": config.AUTHORIZATION
}

# IMAGE/POSTER SETTINGS
secure_base_url = "https://image.tmdb.org/t/p/"

# select size and add to the end of secure_base_url
poster_size = [
    "w92",
    "w154",
    "w185",
    "w342",
    "w500",
    "w780",
    "original"
]

# correct poster base_url e.g.
poster_base_url = "https://image.tmdb.org/t/p/w500"


# CREATE TABLE

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Movie(db.Model):
    __tablename__ = "movie"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True)
    year: Mapped[int] = mapped_column(Integer())
    description: Mapped[str] = mapped_column(String(400))
    rating: Mapped[float] = mapped_column(Float(), nullable=True)
    ranking: Mapped[int] = mapped_column(Integer(), nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=True)

    def __repr__(self) -> str:
        return f"title={self.title!r}"


with app.app_context():
    db.create_all()


# with app.app_context():

#     new_movie = Movie(
#         title="Phone Booth",
#         year=2002,
#         description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or recieve outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#         rating=7.3,
#         ranking=10,
#         review="My favourite character was the caller.",
#         img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
#     )

#     new_movie = Movie(
#         title="Avatar The Way of Water",
#         year=2022,
#         description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#         rating=7.3,
#         ranking=9,
#         review="I liked the water.",
#         img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
#     )

#     db.session.add(new_movie)
#     db.session.commit()


class RateMovieForm(FlaskForm):
    rating = StringField(
        label="Your Rating out of 10 e.g. 7.5", validators=[DataRequired()])
    review = StringField(label="Your Review", validators=[DataRequired()])
    submit = SubmitField(label="Done")


class AddMovieForm(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField(label="Add Movie")


@app.route("/")
def home():
    all_movies = db.session.execute(
        db.select(Movie).order_by(Movie.rating.desc())).scalars().all()

    for idx, movie in enumerate(all_movies):
        # print(idx + 1)
        movie.ranking = idx + 1

        db.session.commit()

    return render_template("index.html",
                           all_movies=all_movies)


@app.route("/add", methods=("GET", "POST"))
def add():

    form = AddMovieForm()

    if form.validate_on_submit():
        title = request.form['title']
        resp = requests.get(
            url=f"https://api.themoviedb.org/3/search/movie?query={title}", headers=HEADERS)
        results = resp.json()["results"]
        session["movie"] = session.get("movie", 0) + 1
        # print(resp.status_code)

        return render_template("select.html",
                               results=results)

    else:
        # the following code can be put inside a route decorator
        # and method

        movie_id = request.args.get("id")
        if movie_id:

            response = requests.get(
                url=f"https://api.themoviedb.org/3/movie/{movie_id}", headers=HEADERS)
            results = response.json()

            # print(results)
            year, month, day = results["release_date"].split("-")

            add_new_movie = Movie(
                title=results["original_title"],
                img_url=poster_base_url + results["poster_path"],
                year=int(year),
                description=results["overview"])

            # print(title)
            # print(img_url)
            # print(year)
            # print(description)

            try:
                db.session.add(add_new_movie)
                db.session.commit()
                return redirect(url_for('edit', id=add_new_movie.id))
            except ValueError:
                print("Problem saving movie title.")

    return render_template("add.html",
                           form=form)


@app.route("/edit/<int:id>", methods=("GET", "POST"))
def edit(id):

    form = RateMovieForm()
    update_field = db.get_or_404(Movie, ident=id)

    if form.validate_on_submit():
        update_field.rating = request.form['rating']
        update_field.review = request.form['review']

        try:
            db.session.commit()
            return redirect(url_for('home'))
        except ValueError:
            print("There was a problem updating to the Database.")

    return render_template("edit.html",
                           form=form,
                           update_field=update_field)


@app.route("/delete/<int:id>", methods=("GET", "POST"))
def delete(id):

    delete_field = db.get_or_404(Movie, ident=id)

    db.session.delete(delete_field)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
