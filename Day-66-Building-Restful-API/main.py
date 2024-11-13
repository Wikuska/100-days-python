import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

app = Flask(__name__)

# Create Database
class Base(DeclarativeBase):
    pass

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    """Data model, defining the schema for the cafe table in the database."""
    # Table Columns with data types and constraints
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

    def to_dict(self):
        """Converts the model instance into a dictionary format."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# with app.app_context():
#     db.create_all()


@app.route("/")
def home():
    """Home route rendering an index.html template."""
    return render_template("index.html")

# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    """Endpoint to fetch a random cafe record from the database."""
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe = {
        "id": random_cafe.id,
        "name": random_cafe.name,
        "map_url": random_cafe.map_url,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,
        "seats": random_cafe.seats,
        "has_toilet": random_cafe.has_toilet,
        "has_wifi": random_cafe.has_wifi,
        "has_sockets": random_cafe.has_sockets,
        "can_take_calls": random_cafe.can_take_calls,
        "coffee_price": random_cafe.coffee_price,
    })
    # Alternative way:
    # return jsonify(cafe=random_cafe.to_dict())

@app.route("/all")
def get_all_cafes():
    """Endpoint to fetch all cafe records, sorted by name."""
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])

@app.route("/search")
def get_cafes_in_location():
    """Endpoint to fetch all cafes in a specific location."""
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(cafes = [cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error = {
            "Not Found": "Sorry, we don't have a cafe at that location"}), 404


# HTTP POST - Create Record
@app.route("/add", methods = ["POST"])
def post_new_cafe():
    """Endpoint to add a new cafe to the database."""
    new_cafe = Cafe(
        name = request.form.get("name"),
        map_url = request.form.get("map_url"),
        img_url = request.form.get("img_url"),
        location = request.form.get("loc"),
        has_sockets = bool(request.form.get("sockets")),
        has_toilet = bool(request.form.get("toilet")),
        has_wifi = bool(request.form.get("wifi")),
        can_take_calls = bool(request.form.get("calls")),
        seats = request.form.get("seats"),
        coffee_price = request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."}), 200

# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods = ["PATCH"])
def update_price(cafe_id):
    """Endpoint to update the coffee price of a specific cafe by its ID.

    Path Parameter:
        cafe_id (int): ID of cafe to update
    Query Parameter:
        new-price (str): New price of the coffee"""
    updated_price = request.args.get("new-price")
    cafe = db.session.get(Cafe, cafe_id)
    if cafe:
        cafe.coffee_price = updated_price
        db.session.commit()
        return jsonify(respose={
            "success": "Successfully updated the price."}), 200
    else:
        return jsonify(error={
            "Not Found": "Sorry, a cafe with that id was not found in the database"}), 404

# HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>", methods = ["DELETE"])
def delete_cafe(cafe_id):
    """Endpoint to delete a cafe from the database using its ID.

    Path Parameter:
        cafe_id (int): ID of cafe to delete
    Query Parameter:
        api-key (str): API key required to authorise the delete action"""
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        cafe = db.session.get(Cafe, cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(respose={
                "success": "Successfully deleted cafe from the database."}), 200
        else:
            return jsonify(error={
                "Not Found": "Sorry, a cafe with that id was not found in the database"}), 404
    else:
        return jsonify(error={
            "Forbidden": "Sorry, that's not allowed. Make sure you have the correct api-key"}), 403

if __name__ == '__main__':
    app.run(debug=True)
