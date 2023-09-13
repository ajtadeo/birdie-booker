import os
import sqlite3
from flask import Blueprint, render_template
from datetime import datetime, timedelta

birdie_booker = Blueprint("birdie-booker", __name__)

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

@birdie_booker.route("/")
def dashboard():
	# get alerts
	conn, cursor = getDB()
	alerts = conn.execute("SELECT * FROM `alerts`").fetchall()
	print(alerts)
	conn.close()

	# get contentAdder options
	players = [i for i in range(1, 5)]
	times = []
	start = datetime(2000, 1, 1, 0)
	for i in range(24):
		times.append((start + timedelta(minutes=30*i)).strftime("%H:%M"))

	return render_template("birdie_booker.html", data=alerts)