import os
import sqlite3
from flask import Blueprint, render_template, redirect, url_for
from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import Form, DateField, SelectField, TimeField
from wtforms.validators import InputRequired, ValidationError

LOCATIONS = [
	(0, 'Recreation Park 18 Golf Course')
]

birdie_booker = Blueprint("birdie-booker", __name__, template_folder='templates')

def getDB():
	path = os.path.dirname(__file__)
	conn = sqlite3.connect(os.path.join(path, "alerts.db"))
	cursor = conn.cursor()
	return conn, cursor

def save(location, numPlayers, date, startTime, endTime, isExpired):
	print(f"Saving Alert: {location}, {numPlayers}, {date}, {startTime}, {endTime}, {isExpired}")
	sql = """
	INSERT INTO `alerts` (`location`, `numPlayers`, `date`, `startTime`, `endTime`, `isExpired`)
	VALUES (?, ?, ?, ?, ?, ?)
	"""
	try:
		conn, cursor = getDB()
		cursor.execute(sql, (location, numPlayers, date, startTime, endTime, isExpired))
		conn.commit()
		conn.close()
	except Exception as err:
		print("Saving to DB failed.")
		print(err)
 
def validate_date(form, date):
	if date.data < datetime.today().date():
		raise ValidationError("Date must be today or a future date.")

def validate_endTime(form, endTime):
	if endTime.data <= form.startTime.data:
		raise ValidationError("End Time must be after start time.")
 
class AlertForm(FlaskForm):
	location = SelectField('Location', [
		InputRequired()
	], choices=LOCATIONS)

	numPlayers = SelectField('Number of Players', [
		InputRequired()
	], choices=[(1, 1), (2, 2), (3, 3), (4, 4)])

	date = DateField('Date', [
		InputRequired(),
		validate_date
	])

	startTime = TimeField('Start Time', [
		InputRequired()
  ])

	endTime = TimeField('End Time', [
		InputRequired(),
		validate_endTime
  ])


@birdie_booker.route("/", methods=['GET', 'POST'])
def birdie_booker_view():
	# get alerts
	conn, cursor = getDB()
	alerts = conn.execute("SELECT * FROM `alerts`").fetchall()
	conn.close()

	print(alerts[0][1])
	print(LOCATIONS[int(alerts[0][1])][1])
 
	# handle form submission
	form = AlertForm()
	if form.validate_on_submit():
		location = form.location.data
		numPlayers = form.numPlayers.data
		date = form.date.data.strftime("%a %m/%d/%Y")
		startTime = form.startTime.data.strftime("%I:%M %p")
		endTime = form.endTime.data.strftime("%I:%M %p")
		isExpired = 0  # form validation requires date to be un-expired

		save(location=location, numPlayers=numPlayers, date=date, startTime=startTime, endTime=endTime, isExpired=isExpired)
		return redirect(url_for("birdie-booker.birdie_booker_view"))

	# TODO: alerts not showing up , possibly because of None value in the database. need to crate validation functions
	return render_template("birdie_booker.html", data=alerts, form=form, locations=LOCATIONS)