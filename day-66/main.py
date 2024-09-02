import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean


app = Flask(__name__)

# CREATE DB


class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


def serialize_to_dict(model):
    """Utility function that takes SQLAlchemy model instance and converts to dictionary"""
    return {column.name: getattr(model, column.name) for column in model.__table__.columns}


@ app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@ app.route("/random")
def get_random():
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()

    # convert each row of the query results into dict
    # each columns name and value are mapped to dict key:value
    # Use the model to get columns from the table

    # option 1
    results = [serialize_to_dict(cafes) for cafes in all_cafes]
    random_cafe = random.choice(results)
    return jsonify(random_cafe)

    # option 2
    # results = [{column.name: getattr(
    #     row, column.name) for column in Cafe.__table__.columns} for row in all_cafes]
    # # return results
    # random_cafe = random.choice(results)
    # # print(random_cafe)
    # return jsonify(random_cafe)

    # option 3
    # random_cafe = random.choice(all_cafes)
    # print(random_cafe.__dict__)
    # random_cafe.__dict__.pop("_sa_instance_state")
    # return jsonify(random_cafe.__dict__)

    # return jsonify([{"id": user.id, "name": user.name} for user in get_cafes])


@app.route("/all")
def get_all():
    all_cafes = db.session.execute(db.select(Cafe)).scalars()

    results = [serialize_to_dict(cafes) for cafes in all_cafes]
    return jsonify(results)


@app.route("/search")
def search():
    # loc = "Peckham"
    loc = request.args.get("loc")
    # print(loc)

    search_cafe_loc = db.session.execute(
        db.select(Cafe).where(Cafe.location == loc)).scalars().all()

    # option 1
    # location_dict = [area.__dict__ for area in search_cafe_loc]
    # # print(location_dict)

    # #  remove the '_sa_instance_state' attribute
    # for row in location_dict:
    #     row.pop("_sa_instance_state", None)

    # return jsonify(location_dict)

    # option 2
    if search_cafe_loc:
        location_dict = [serialize_to_dict(area) for area in search_cafe_loc]
        return jsonify(location_dict)
    else:
        return jsonify([{"error": {"Not Found": "Sorry, we don't have a cafe at that location."}}])


@app.route("/add", methods=["POST"])
def add():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        seats=request.form.get("seats"),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        has_sockets=bool(request.form.get("sockets")),
        can_take_calls=bool(request.form.get("calls")),
        coffee_price=request.form.get("coffee_price")
    )

    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


@app.route("/update-price/<int:id>", methods=["PATCH"])
def update(id):

    new_amount = request.args.get("new_price")
    update_price = db.get_or_404(Cafe, ident=id)

    if update_price:
        update_price.coffee_price = new_amount
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."})
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})


@app.route("/report-closed/<int:id>", methods=["DELETE"])
def delete(id):
    api = request.args.get("api-key")
    db_record = db.get_or_404(Cafe, ident=id)

    if not api:
        return jsonify(error={"error": "Sorry that's not allowed. Make sure you have the correct api_key."})

    if not db_record:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})

    if api and db_record:
        db.session.delete(db_record)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the database record."})



if __name__ == '__main__':
    app.run(debug=True)
