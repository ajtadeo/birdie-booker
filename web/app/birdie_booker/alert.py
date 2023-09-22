import os
import sqlite3
from datetime import datetime, timedelta

def init_alerts():
	path = os.path.dirname(__file__)
	conn = sqlite3.connect(os.path.join(path, "birdie_booker.db"))
	cursor = conn.cursor()
	sql = """
	CREATE TABLE IF NOT EXISTS `alerts` (
		`id` INTEGER PRIMARY KEY,
		`location` INTEGER,
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

def get_alerts():
	try:
		path = os.path.dirname(__file__)
		conn = sqlite3.connect(os.path.join(path, "birdie_booker.db"))
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
		conn = sqlite3.connect(os.path.join(path, "birdie_booker.db"))
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
		conn = sqlite3.connect(os.path.join(path, "birdie_booker.db"))
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
		conn = sqlite3.connect(os.path.join(path, "birdie_booker.db"))
		cursor = conn.cursor()
		cursor.execute(sql)
		conn.commit()
		conn.close()
	except Exception as err:
		print("Deleting alert from DB failed.")
		print(err)