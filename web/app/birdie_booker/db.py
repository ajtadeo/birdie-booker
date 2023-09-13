import os
import sqlite3

path = os.path.dirname(__file__)
CONN = sqlite3.connect(os.path.join(path, "alerts.db"))
CURSOR = CONN.cursor()