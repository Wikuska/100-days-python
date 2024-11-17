from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Flask app and configure basic settings
app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = os.getenv['APP_SECRET_KEY']
Bootstrap5(app)

# Initialize SQLAlchemy and create base model for database
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# BlogPost model which represents each post record in the database
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

# with app.app_context():
#     db.create_all()

# Configure form
class CreatePostForm(FlaskForm):
    title = StringField('Post title', validators=[DataRequired()])
    subtitle = StringField('Post subtitle', validators=[DataRequired()])
    author = StringField('Post author name', validators=[DataRequired()])
    img_url = StringField('Post background image url', validators=[DataRequired(), URL()])
    body = CKEditorField('Post content', validators=[DataRequired()])
    submit = SubmitField('Submit Post') 

@app.route('/')
def get_all_posts():
    """Home route rendering an index.html template and passing all BlogPost data from database."""
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    """Post route rendering a post.html template and passing retrieved BlogPost from the database based on the post_id"""
    requested_post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    return render_template("post.html", post=requested_post)


@app.route('/new-post', methods = ("POST", "GET"))
def create_new_post():
    """New-post route rendering a make-post.html template with CreatePostForm"""
    form = CreatePostForm()
    # After submiting form, new BlogPost is added to database
    if form.validate_on_submit():
        new_post = BlogPost(
            title = form.title.data,
            subtitle = form.subtitle.data,
            date = date.today().strftime("%B %d, %Y"),
            body = form.body.data,
            author = form.author.data,
            img_url = form.img_url.data
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form = form)

@app.route('/edit-post/<int:post_id>', methods = ("POST", "GET"))
def edit_post(post_id):
    """Edit-post route rendering the make-post.html template with a pre-filled CreatePostForm containing the data of the BlogPost based on post_id"""
    post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    edit_form = CreatePostForm(
        title = post.title,
        subtitle = post.subtitle,
        author = post.author,
        img_url = post.img_url,
        body = post.body
    )
    # After submitting form, update BlogPost data
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.date = post.date
        post.body = edit_form.body.data
        post.author = edit_form.author.data
        post.img_url = edit_form.img_url.data
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", edit = True, form = edit_form)

@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    """Delete route deleting BlogPost from the database based on the post_id"""
    post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("get_all_posts"))

# Code below wasn't changed
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
