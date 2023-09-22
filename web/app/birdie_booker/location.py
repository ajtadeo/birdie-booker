import os
import sqlite3

def init_locations():
  path = os.path.dirname(__file__)
  conn = sqlite3.connect(os.path.join(path, "birdie_booker.db"))
  cursor = conn.cursor()
  sql = """
  CREATE TABLE IF NOT EXISTS `locations` (
    `id` INTEGER PRIMARY KEY,
    `name` TEXT,
    `city` TEXT
  )
  """
  cursor.execute(sql)
  conn.commit()
  conn.close()
  
def get_locations():
	try:
		path = os.path.dirname(__file__)
		conn = sqlite3.connect(os.path.join(path, "birdie_booker.db"))
		cursor = conn.cursor()
		locations = conn.execute("SELECT * FROM `locations`").fetchall()
		conn.close()
	except Exception as err:
		print("Fetching locations from DB failed.")
		print(err)
	return locations
  
def save_location(name, city):
	print(f"Saving location: {name}")
	sql = f"""
	INSERT INTO `locations` (`name`, `city`)
	VALUES ('{name}', '{city}')
	"""
	try:
		path = os.path.dirname(__file__)
		conn = sqlite3.connect(os.path.join(path, "birdie_booker.db"))
		cursor = conn.cursor()
		cursor.execute(sql)
		conn.commit()
		conn.close()
	except Exception as err:
		print("Saving location to DB failed.")
		print(err)
  
def delete_location(id):
	print(f"Deleting location: {id}")
	sql = f"""
	DELETE FROM `locations`
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
		print("Deleting location from DB failed.")
		print(err)