from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app, configure Flask-login and gravatar
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("APP_KEY")
ckeditor = CKEditor(app)
Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

gravatar = Gravatar(app)

# Create database
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Configure tables
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates = "posts")
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    comments = relationship("Comment", back_populates = "parent_post")

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(1000), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")

class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(1000))
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates = "comments")
    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates = "comments")

with app.app_context():
    db.create_all()


def admin_only(func):
    """Decorator to restrict access to admin-only routes"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("login"))
        if current_user.id != 1:
            abort(403)
        return func(*args, **kwargs)
    return decorated_view


@app.route('/register', methods = ("POST", "GET"))
def register():
    """Route handling user registration by rendering template with RegisterForm and adding new User to database on validated form submission"""
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user_exists = db.session.execute(db.select(User).where(User.email == register_form.email.data)).scalar()
        if not user_exists:
            new_user = User(
                email = register_form.email.data,
                password = generate_password_hash(register_form.password.data, method = "pbkdf2", salt_length = 8),
                name = register_form.name.data
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("get_all_posts"))
        else:
            flash("You are already registered with this email. Log in instead!")
            return redirect(url_for("login"))
    return render_template("register.html", form = register_form)


@app.route('/login', methods = ("POST", "GET"))
def login():
    """Route handling user login by rendering template with LoginForm, validating input, and processing login logic"""
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == login_form.email.data)).scalar()
        if not user:
            flash("Email not found")
            return redirect(url_for('login'))
        if not check_password_hash(user.password, login_form.password.data):
            flash("Wrong password")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for("get_all_posts"))
    return render_template("login.html", form = login_form)


@app.route('/logout')
def logout():
    """Logout route logging out current user and redirecting to main page """
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    """Get-all-posts route rendering index.html template with all posts from database"""
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    """Show_post route rendering a post.html template with requested_post and CommentForm. Handles comments submission"""
    requested_post = db.get_or_404(BlogPost, post_id)
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            new_comment = Comment(
                text = form.comment.data,
                comment_author = current_user,
                parent_post = requested_post
            )
            db.session.add(new_comment)
            db.session.commit()
        else:
            flash("You must be logged in to submit comments")
            return redirect(url_for("login"))
    return render_template("post.html", post=requested_post, form=form)


@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    """Route handling new post creation. Renders template with CreatePostForm and creates new BlogPost in database on validated form submission"""
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


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    """Route handling edition of an existing BlogPost, fetches the post by post_id, pre-fills the form and updates BlogPost in database on validated form submission"""
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


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    """Fetches the post by post_id and deletes it from database"""
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
