from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("APP_KEY")
Bootstrap5(app)

class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Project(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    topic: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    image: Mapped[str] = mapped_column(String, nullable=False)
    github: Mapped[str] = mapped_column(String, nullable=False)

class EmailForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send a message")

@app.route("/", methods = ("POST", "GET"))
def home():
    form = EmailForm()
    if form.validate_on_submit():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user = os.getenv('MY_MAIL'), password = os.getenv('MY_PASSWORD'))
            connection.sendmail(
                from_addr = os.getenv('MY_MAIL'),
                to_addrs = os.getenv('MY_MAIL'),
                msg = f"Subject: New portfolio mail\n\nFrom: {form.name.data}\nUser email: {form.email.data}\nMessage: {form.message.data}"
            )
            flash("Email sent!")
            return redirect(url_for("home"))
    return render_template("index.html", form = form)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
