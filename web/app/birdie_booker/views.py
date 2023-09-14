import os
import sqlite3
from flask import Blueprint, render_template, redirect
from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import Form, DateField, SelectField, TimeField, validators

LOCATIONS = [
	(0, 'Recreation Park 18 Golf Course')
]

birdie_booker = Blueprint("birdie-booker", __name__, template_folder='templates')

def getDB():
	path = os.path.dirname(__file__)
	conn = sqlite3.connect(os.path.join(path, "alerts.db"))
	cursor = conn.cursor()
	return conn, cursor

def save(location, numPlayers, date, startTime, endTime):
	print(f"Saving Alert: {location}, {numPlayers}, {date}, {startTime}, {endTime}")
	sql = """
	INSERT INTO `alerts` (`location`, `numPlayers`, `date`, `startTime`, `endTime`)
	VALUES (?, ?, ?, ?, ?)
	"""
	conn, cursor = getDB()
	cursor.execute(sql, (location, numPlayers, date, startTime, endTime))
	conn.commit()
	conn.close()
 
class AlertForm(FlaskForm):
	location = SelectField('Location', choices=LOCATIONS)
	numPlayers = SelectField('Number of Players', choices=[(1, 1), (2, 2), (3, 3), (4, 4)])
	date = DateField('Date', format='%m/%d/%Y')
	startTime = TimeField('Start Time')
	endTime = TimeField('End Time')


@birdie_booker.route("/", methods=['GET', 'POST'])
def birdie_booker_view():
	# get alerts
	conn, cursor = getDB()
	alerts = conn.execute("SELECT * FROM `alerts`").fetchall()
	print(alerts)
	conn.close()
 
	# handle form submission
	form = AlertForm()
	if form.is_submitted():
		location = form.location.data
		numPlayers = form.numPlayers.data
		date = form.date.data.strftime("%m/%d/%Y")
		startTime = form.startTime.data.strftime("%H:%M")
		endTime = form.endTime.data.strftime("%H:%M")

		save(location=location, numPlayers=numPlayers, date=date, startTime=startTime, endTime=endTime)
		return redirect("/")

	# TODO: alerts not showing up , possibly because of None value in the database. need to crate validation functions
	return render_template("birdie_booker.html", alerts=alerts, form=form)