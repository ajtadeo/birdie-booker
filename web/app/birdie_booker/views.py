import os
import sqlite3
from flask import Blueprint, render_template, redirect, url_for
from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import Form, DateField, SelectField, TimeField, IntegerField
from wtforms.validators import InputRequired, ValidationError

LOCATIONS = [
	(0, 'Recreation Park 18 Golf Course')
]

birdie_booker = Blueprint("birdie-booker", __name__, template_folder='templates')

def get_alerts():
	try:
		path = os.path.dirname(__file__)
		conn = sqlite3.connect(os.path.join(path, "alerts.db"))
		cursor = conn.cursor()
		alerts = conn.execute("SELECT * FROM `alerts`").fetchall()
		conn.close()
	except Exception as err:
		print("Fetching alerts from DB failed.")
		print(err)
	return alerts

def save_alert(location, numPlayers, date, startTime, endTime, isExpired):
	print(f"Saving alert: {location}, {numPlayers}, {date}, {startTime}, {endTime}, {isExpired}")
	sql = """
	INSERT INTO `alerts` (`location`, `numPlayers`, `date`, `startTime`, `endTime`, `isExpired`)
	VALUES (?, ?, ?, ?, ?, ?)
	"""
	try:
		path = os.path.dirname(__file__)
		conn = sqlite3.connect(os.path.join(path, "alerts.db"))
		cursor = conn.cursor()
		cursor.execute(sql, (location, numPlayers, date, startTime, endTime, isExpired))
		conn.commit()
		conn.close()
	except Exception as err:
		print("Saving alert to DB failed.")
		print(err)

def delete_alert(id):
	print(f"Deleting alert: {id}")
	sql = f"""
	DELETE FROM `alerts`
	WHERE id = {id}
	"""
	try:
		path = os.path.dirname(__file__)
		conn = sqlite3.connect(os.path.join(path, "alerts.db"))
		cursor = conn.cursor()
		cursor.execute(sql)
		conn.commit()
		conn.close()
	except Exception as err:
		print("Deleting alert from DB failed.")
		print(err)

def set_expired_alert(id):
	print(f"Setting expired alert: {id}")
	sql = f"""
	UPDATE `alerts`
	SET `isExpired` = 1
	WHERE id = {id}
	"""
	try:
		path = os.path.dirname(__file__)
		conn = sqlite3.connect(os.path.join(path, "alerts.db"))
		cursor = conn.cursor()
		cursor.execute(sql)
		conn.commit()
		conn.close()
	except Exception as err:
		print("Deleting alert from DB failed.")
		print(err)
 
def validate_date(form, date):
	if date.data < datetime.today().date():
		raise ValidationError("Date must be today or a future date.")

def validate_endTime(form, endTime):
	if endTime.data <= form.startTime.data:
		raise ValidationError("End Time must be after start time.")
 
class AddForm(FlaskForm):
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

class DeleteForm(FlaskForm):
	id = IntegerField()

@birdie_booker.route("/")
def index():
	alerts = get_alerts()
	print(alerts)
	# save_alert(0, 4, 'Wed 09/13/2023', '07:00 AM', '08:00 AM', 0)
 
	for alert in alerts:
		if alert[6] == 0 and datetime.strptime(alert[3], "%a %m/%d/%Y").date() < datetime.today().date():
			set_expired_alert(alert[0])
 
	# register forms
	add_form = AddForm()
	delete_form = DeleteForm()
	
	return render_template("birdie_booker.html", data=alerts, add_form=add_form, delete_form=delete_form, locations=LOCATIONS)

@birdie_booker.route("/add", methods=['POST'])
def add():
	alerts = get_alerts()

	# register forms
	add_form = AddForm()
	delete_form = DeleteForm()

	# handle add_form
	if add_form.validate_on_submit():
		location = add_form.location.data
		numPlayers = add_form.numPlayers.data
		date = add_form.date.data.strftime("%a %m/%d/%Y")
		startTime = add_form.startTime.data.strftime("%I:%M %p")
		endTime = add_form.endTime.data.strftime("%I:%M %p")
		isExpired = 0  # form validation requires date to be un-expired

		save_alert(location=location, numPlayers=numPlayers, date=date, startTime=startTime, endTime=endTime, isExpired=isExpired)
		return redirect(url_for("birdie-booker.index"))

	return render_template("birdie_booker.html", data=alerts, add_form=add_form, delete_form=delete_form, locations=LOCATIONS)

@birdie_booker.route("/delete", methods=['POST'])
def delete():
	alerts = get_alerts()

	# register forms
	add_form = AddForm()
	delete_form = DeleteForm()

	# handle delete_form
	if delete_form.is_submitted():
		id = delete_form.id.data
		delete_alert(id)
		return redirect(url_for("birdie-booker.index"))
	
	return render_template("birdie_booker.html", data=alerts, add_form=add_form, delete_form=delete_form, locations=LOCATIONS)