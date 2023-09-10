from flask import Flask, render_template
import sqlite3
import os

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
 
# intialize app
app = Flask(__name__)

# intialize database
path = os.path.dirname(__file__)
conn, cursor = getDB()
sql = """
CREATE TABLE IF NOT EXISTS `alerts` (
	`id` INTEGER PRIMARY KEY,
	`location` TEXT,
	`numPlayers` INTEGER,
	`date` TEXT,
	`startTime` TEXT,
	`endTime` TEXT,
	`isExpired` INTEGER DEFAULT 0
)
"""
cursor.execute(sql)
conn.commit()
conn.close()

# routes
@app.route('/')
def index():
	return render_template("index.html")

@app.route('/birdie-booker')
def birdieBooker():
	conn, cursor = getDB()
	alerts = conn.execute("SELECT * FROM `alerts`").fetchall()
	print(alerts)
	conn.close()
	return render_template("birdieBooker.html", data=alerts)