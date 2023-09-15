import os
import sqlite3

# initialize database
path = os.path.dirname(__file__)
conn = sqlite3.connect(os.path.join(path, "alerts.db"))
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