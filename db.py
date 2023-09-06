import sqlite3
import os

# setup database connection
path = os.path.dirname(__file__)
CONN = sqlite3.connect(os.path.join(path, "alerts.db"))
CURSOR = CONN.cursor()