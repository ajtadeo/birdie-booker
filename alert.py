from datetime import date, time
from location import Location
import os
import requests

# chrome driver/selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

# sqlite3
from db import CONN, CURSOR
import sqlite3

class Alert:  
  # responsibility of the entire class, not individual instances
  # NOTE: date is a special keyword in SQL, so we have to surround the col name with backticks ``
  @classmethod
  def createTable(self):
    sql = """
      CREATE TABLE IF NOT EXISTS `alerts` (
        `id` INTEGER PRIMARY KEY,
        `location` TEXT,
        `numPlayers` INTEGER,
        `date` TEXT,
        `startTime` TEXT,
        `endTime` TEXT
      )
    """
    CURSOR.execute(sql)
    CONN.commit()
    
  def __init__(self):
    """ used for production only """
    self.setSettings()
  
  # def __init__(self, location, numPlayers, date, startTime, endTime):
  #   """ used for development/testing only """
  #   self.location = location
  #   self.numPlayers = numPlayers
  #   self.date = date
  #   self.startTime = startTime
  #   self.endTime = endTime
      
  def save(self):
    """ this method saves the setting values for an instance of Alert to alerts.db, then sets self.id to the primary key """
    self.createTable()
    sql = """
      INSERT INTO `alerts` (`location`, `numPlayers`, `date`, `startTime`, `endTime`)
      VALUES (?, ?, ?, ?, ?)
    """
    CURSOR.execute(sql, (self.location, self.numPlayers, self.date, self.startTime, self.endTime))
    self.id = CURSOR.execute("SELECT last_insert_rowid() FROM `alerts`").fetchone()[0]
    CONN.commit()
  
  def setSettings(self):
    """ Sets location, numPlayers, date, startTime, and endTime variables """
    # get location
    while True:
      try:
        for loc in Location:
          print(f"{loc.value}) {loc.name}")
        self.location = int(input("Enter the location ID: "))
        if self.location < 0 or self.location > len(Location) - 1:
          raise ValueError
      except:
        print(f"\nSorry, location ID must be an integer between 0 and {len(Location) - 1}")
      else:
        break
      
    # get number of players
    while True:
      try:
        self.numPlayers = int(input("Enter the number of players: "))
        if self.numPlayers < 1 or self.numPlayers > 4:
          raise ValueError
      except ValueError:
        print("\nSorry, player number must an integer between 1 and 4.")
        continue
      else:
        break
      
    # get date
    while True:
      try:
        dateRaw = date.fromisoformat(input("Enter the booking date (YYYY-MM-DD): "))
        if dateRaw < date.today():
          raise ValueError
        self.date = str(dateRaw)
      except ValueError:
        print("\nSorry, date was invalid or in an invalid format.")
        continue
      else:
        break
      
    # get start time
    while True:
      try:
        startTimeRaw = time.fromisoformat(input("Enter start time (HH:MM, 24hr): "))
        self.startTime = str(startTimeRaw)
      except ValueError:
        print("\nSorry, start time was invalid or in an invalid format.")
        continue
      else:
        break
      
      # get end time
    while True:
      try:
        endTimeRaw = time.fromisoformat(input("Enter end time (HH:MM, 24hr): "))
        if endTimeRaw < startTimeRaw:
          raise ValueError
        self.endTime = str(endTimeRaw)
      except ValueError:
        print("\nSorry, end time was before start time or in an invalid format.")
        continue
      else:
        break
      
    # confirm settings
    confirmMsg = ("-------------------\n"
                  f"Location:\t{Location(self.location).name}\n"
                  f"Players:\t{self.numPlayers}\n"
                  f"Date:\t\t{self.date}\n"
                  f"Start Time:\t{self.startTime}\n"
                  f"End Time:\t{self.endTime}\n"
                  "-------------------\n"
                  "Confirm these settings? (y/n): ")
    result = input(confirmMsg)
    while result != "n" and result != "y":
      print("\nSorry, that input is invalid.")
      result = input(confirmMsg)
    if result.lower() == "n":
      updateSettings()
      
  def printSettings(self):
    msg = ("-------------------\n"
          f"Location:\t{Location(self.location).name}\n"
          f"Players:\t{self.numPlayers}\n"
          f"Date:\t\t{self.date}\n"
          f"Start Time:\t{self.startTime}\n"
          f"End Time:\t{self.endTime}\n"
          "-------------------")
    print(msg)