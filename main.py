from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_secret_key'
Bootstrap(app)

# This form will be used to add a new coffee resturant to the cafe-data.csv file.
class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), URL()])
    open = StringField('Open', validators=[DataRequired()])
    close = StringField('Close', validators=[DataRequired()])
    coffee = SelectField('Coffee', choices = ["☕","☕☕","☕☕☕","☕☕☕☕","☕☕☕☕☕"], validators=[DataRequired()])
    wifi = SelectField('Wifi', choices = ["💪","💪💪","💪💪💪","💪💪💪💪","💪💪💪💪💪"], validators=[DataRequired()])
    power = SelectField('Power', choices = ["🔌","🔌🔌","🔌🔌🔌","🔌🔌🔌🔌","🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")

# This is a secret endpoint, used to add resturants.
@app.route('/add', methods = ["GET","POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        new_data = f"{form.cafe.data},{form.location.data},{form.open.data},{form.close.data},{form.coffee.data},{form.wifi.data},{form.power.data}"
        with open(file = 'cafe-data.csv', mode = 'a', encoding = "utf8") as csv_file:
            csv_file.write("\n" + new_data)
    return render_template('add.html', form = form)

# Endpoint to see list of all cafes.
@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding = "utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)