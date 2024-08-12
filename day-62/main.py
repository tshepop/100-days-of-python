from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap4
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, URL
import csv


app = Flask(__name__)
app.secret_key = 'ad5bfc33dc9f86ec12a70ebacf4187780d030bc417d158dbe2992de773d09bf2'

Bootstrap4(app)
app.config["BOOTSTRAP_SERVE_LOCAL"] = True


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[InputRequired()])
    location = StringField('Cafe Location on Google Maps(URL)',
                           validators=[InputRequired(), URL()])
    open_time = StringField('Opening Time e.g. 9AM',
                            validators=[InputRequired()])
    close_time = StringField('Closing Time e.g. 5PM',
                             validators=[InputRequired()])
    coffee_rating = SelectField('Coffee Rating',
                                validators=[InputRequired()],
                                choices=['☕️' * i for i in range(0, 6)],
                                validate_choice=True)
    wifi_rating = SelectField('Wifi Strength Rating',
                              validators=[InputRequired()],
                              choices=['✘' if i == 0 else '💪' *
                                       i for i in range(0, 6)],
                              validate_choice=True)
    power_rating = SelectField('Power Socket Availability',
                               validators=[InputRequired()],
                               choices=['✘' if i == 0 else
                                        '🔌' * i for i in range(0, 6)],
                               validate_choice=True)
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=("GET", "POST"))
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        # print("True")

        with open("cafe-data.csv", "a") as csvfile:
            data_write = csv.writer(csvfile)

            data_write.writerow([form.cafe.data,
                                 form.location.data,
                                 form.open_time.data,
                                 form.close_time.data,
                                 form.coffee_rating.data,
                                 form.wifi_rating.data,
                                 form.power_rating.data,])

        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)

    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
