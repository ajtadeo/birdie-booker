import sqlite3

# setup database connection
print("Connecting to database")
CONN = sqlite3.connect("alerts.db")
CURSOR = CONN.cursor()