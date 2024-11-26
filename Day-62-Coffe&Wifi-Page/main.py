from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, URLField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, URL
import csv
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("APP_KEY")
Bootstrap5(app)

# Creating cafe form element which will be used to add new cafe data on route /add
class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_URL = URLField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    open_time = StringField("Opening time e.g 8AM", validators=[DataRequired()])
    closing_time = StringField("Closing time e.g 5.30PM", validators=[DataRequired()])
    coffee_rating = SelectField(u"Coffee Rating", choices = ["✘","☕","☕☕","☕☕☕","☕☕☕☕","☕☕☕☕☕"], validators=[DataRequired()])
    wifi_rating = SelectField(u"Wifi Strength Rating", choices = ["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"], validators=[DataRequired()])
    power_outlet = SelectField(u"Power Socket Availability", choices = ["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField('Submit')

# Define route for main page
@app.route("/")
def home():
    return render_template("index.html")

# Define route for add page, accepting both GET (initial page load) and POST (form submission) requests
@app.route('/add', methods = ["POST", "GET"])
def add_cafe():
    form = CafeForm()
    # If data in form was submitted and passed validation checks
    if form.validate_on_submit():
        # Open cafe's data file (cafe-data.csv) and append it with data from submitted form
        with open(file = "cafe-data.csv", mode = "a", encoding = "utf-8") as file:
            file.write(f"\n{form.cafe.data},{form.location_URL.data},{form.open_time.data},{form.closing_time.data},{form.coffee_rating.data},{form.wifi_rating.data},{form.power_outlet.data}")
        # Redirect to cafe's page
        return redirect(url_for("cafes"))
    return render_template('add.html', form=form)

# Define route for cafe's page
@app.route('/cafes')
def cafes():
    # Open cafe's data file (cafe-data.csv)
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        # Create list containing lists, each representing row from data file
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        # Render cafe's page and pass list_of_rows
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
