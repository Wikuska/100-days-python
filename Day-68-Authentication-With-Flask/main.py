from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('APP_KEY')
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize SQLAlchemy and create base model for database
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# User model which represents each user record in the database
class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/')
def home():
    """Home route rendering an index.html template and passing information if user is currently logged in."""
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods = ("POST", "GET"))
def register():
    """Register route rendering a register.html template and passing information if user is currently logged in."""
    # If user isn't logged in, they can submit form to register
    if request.method == "POST":
        user_found = db.session.execute(db.select(User).where(User.email == request.form["email"])).scalar()
        # If email provided in the form doesn't already exist in base, create new user
        if not user_found:
            new_user = User(
                email = request.form["email"],
                password = generate_password_hash(request.form["password"], method = "pbkdf2:sha256", salt_length = 8),
                name = request.form["name"]
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("secrets"))
        else:
            flash('Account already registered. Log in instead!')
            return render_template("register.html")
        
    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods = ("POST", "GET"))
def login():
    """Login route rendering a login.html template and passing information if user is currently logged in."""
    if request.method == "POST":
        user = db.session.execute(db.select(User).where(User.email == request.form["email"])).scalar()
        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("secrets"))
        # If user with submitted email doesn't exist
        elif not user:
            flash("Email not found")
            return render_template("login.html")
        # If submitted password isn't same as User password 
        elif not check_password_hash(user.password, request.form["password"]):
            flash("Password is incorrect")
            return render_template("login.html")
    
    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route('/secrets')
@login_required
def secrets():
    """Secrets route rendering a secrets.html template. To reach user is required to be logged in"""
    return render_template("secrets.html", name = current_user.name, logged_in = True)


@app.route('/logout')
def logout():
    """Logout route logging out current user and redirecting to login page """
    logout_user()
    return redirect(url_for("login"))


@app.route('/download')
@login_required
def download():
    """Download route sending file from directory user can download. To reach user is required to be logged in"""
    return send_from_directory('static/files', "cheat_sheet.pdf", as_attachment = True)


if __name__ == "__main__":
    app.run(debug=True)
