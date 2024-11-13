from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Headers for the API requests
HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('TMDB_API_KEY')}"
}

# Initialize Flask app and configure basic settings
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap5(app)

# Initialize SQLAlchemy and create base model for database
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///top-movies.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Movie model which represents each movie record in the database
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    title: Mapped[str] = mapped_column(String, unique = True, nullable = False)
    year: Mapped[int] = mapped_column(Integer, nullable = False)
    description: Mapped[str] = mapped_column(String, nullable = False)
    rating: Mapped[float] = mapped_column(Float, nullable = True)
    ranking: Mapped[int] = mapped_column(Integer, nullable = True)
    review: Mapped[str] = mapped_column(String, nullable = True)
    img_url: Mapped[str] = mapped_column(String, nullable = False)

# with app.app_context():
#     db.create_all()

# Form for updating movie rating and review
class UpdateForm(FlaskForm):
    rating = StringField('Your rating out of 10:', validators = [DataRequired()])
    review = StringField('Change your review:', validators = [DataRequired()])
    submit = SubmitField('Done')
# Form for adding new movie titles
class AddForm(FlaskForm):
    title = StringField('Movie Title', validators = [DataRequired()])
    submit = SubmitField('Add Movie')

# Route to render home page
@app.route("/")
def home():
    # Retrieve movies sorted by rating
    result = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars().all()
    movies_titles = [element.title for element in result]
    for title in movies_titles:
        # Retrieve and update each movie's ranking based on sorted order
        edit = db.session.execute(db.select(Movie).where(Movie.title == title)).scalar()
        edit.ranking = movies_titles.index(title) + 1
        db.session.commit()
    # Retrieve all updated movies to pass to the template
    all_movies = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars().all()
    return render_template("index.html", movies = all_movies)

# Route to update a specific movie's rating and review
@app.route("/update/<int:movie_id>", methods = ["POST", "GET"])
def update(movie_id):
    form = UpdateForm()
    if form.validate_on_submit():
        # Find movie by ID and update rating/review
        movie_to_edit = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
        movie_to_edit.rating = form.rating.data
        movie_to_edit.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=form)

# Route to delete a specific movie from the database
@app.route("/delete/<int:movie_id>")
def delete(movie_id):
    record_to_delete = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
    db.session.delete(record_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

# Route to add a new movie title by searching via API
@app.route("/add", methods = ["POST", "GET"])
def add():
    form = AddForm()
    if form.validate_on_submit():
        # Search for movies using the API with provided title
        params = {"query": form.title.data}
        search_url = "https://api.themoviedb.org/3/search/movie"
        search_response = requests.get(search_url, headers=HEADERS, params=params).json()
        return render_template("select.html", movies = search_response)
    return render_template("add.html", form = form)

# Route to get full movie details using the selected movie's ID and add to database
@app.route("/get-movie-details/<int:movie_id>")
def get_movie_details(movie_id):
    # Step 1: Get external IDs for the movie
    ex_id_response = requests.get(url = f"https://api.themoviedb.org/3/movie/{movie_id}/external_ids", headers=HEADERS).json()
    # Step 2: Use IMDb ID to retrieve detailed information about the movie
    find_by_id_response = requests.get(url = f"https://api.themoviedb.org/3/find/{ex_id_response["imdb_id"]}?external_source=imdb_id", headers=HEADERS).json()
    # Step 3: Add the new movie to the database
    new_movie = Movie(
        title = find_by_id_response["movie_results"][0]["title"],
        year = find_by_id_response["movie_results"][0]["release_date"].split("-")[0],
        description = find_by_id_response["movie_results"][0]["overview"],
        img_url = f"https://image.tmdb.org/t/p/w500{find_by_id_response['movie_results'][0]['poster_path']}"
    )
    db.session.add(new_movie)
    db.session.commit()
    # Redirect to update the new movie's details
    created_movie = db.session.execute(db.select(Movie).where(Movie.title == find_by_id_response["movie_results"][0]["title"])).scalar()
    return redirect(url_for("update", movie_id = created_movie.id))

# Run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
