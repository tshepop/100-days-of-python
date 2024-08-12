from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


app = Flask(__name__)
app.secret_key = "38c041d82001dd7e0425c3301a6f70179f4c4d3f201a1bdb1f5d4fc54e6e574f"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///all-books.db"


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Book(db.Model):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float())

    def __repr__(self) -> str:
        return f"title={self.title!r}"


with app.app_context():
    db.create_all()


# all_books = []


@app.route('/')
def home():

    # error = "Libray is empty."

    all_books = db.session.execute(
        db.select(Book).order_by(Book.id)).scalars().all()

    return render_template("index.html",
                           all_books=all_books)


@app.route("/add", methods=("GET", "POST"))
def add():
    # add_book = {}

    if request.method == "POST":
        book_title = request.form["title"]
        book_author = request.form["author"]
        book_rating = request.form["rating"]

        new_record = Book(title=book_title,
                          author=book_author, rating=book_rating)
        try:
            db.session.add(new_record)
            db.session.commit()
            return redirect(url_for("home"))
        except ValueError:
            print("A problem occured while attempting to save to database.")

        # populate a dict, then append to list
        # if book_title or book_author or book_rating:
        #     add_book["title"] = book_title
        #     add_book["author"] = book_author
        #     add_book["rating"] = book_rating

        #     all_books.append(add_book)

    return render_template("add.html")


@app.route("/edit/<int:id>", methods=("GET", "POST"))
def edit(id):

    field_update = db.get_or_404(Book, ident=id)

    if request.method == "POST":
        field_update.rating = request.form["edit"]

        try:
            db.session.commit()
            return redirect(url_for("home"))
        except ValueError:
            print("Problem with updating.")

    return render_template("edit.html",
                           db_data=field_update)


@app.route("/delete/<int:id>")
def delete(id):

    field_delete = db.get_or_404(Book, ident=id)
    try:
        db.session.delete(field_delete)
        db.session.commit()
        return redirect(url_for("home"))
    except ValueError:
        print("No more items to delete.")


if __name__ == "__main__":
    app.run()
