#!/usr/bin/env python3
from dotenv import load_dotenv
from alert import Alert
from datetime import date, time, datetime
import argparse
from db import CONN, CURSOR
from tabulate import tabulate
from sqlite3 import OperationalError
from webscraper import Webscraper

load_dotenv()

def main():
  parser = argparse.ArgumentParser()
  mode = parser.add_mutually_exclusive_group()
  mode.add_argument("-s", "--scrape", dest="scrape", action="store_true", help="Running web scrapers for Alerts")
  mode.add_argument("-l", "--list", dest="list", action="store_true", help="List existing Alerts")
  args = parser.parse_args()
  
  if args.scrape:
    scrapeMode()
  elif args.list:
    listMode()
  else:
    try:
      print("Creating an Alert...\n\n")
      myAlert = Alert()
      myAlert.save()
    except Exception as e:
      print(e)
      
def scrapeMode():
  print(f"Starting script at: {datetime.now()}\n\n")
  
  # print Alerts
  print("Scraping existing Alerts...")
  records = CURSOR.execute("SELECT * FROM alerts").fetchall()
  headers = ["ID", "Location", "Num Players", "Date", "Start Time", "End Time"]
  print(tabulate(records, headers, tablefmt="grid"))
  if len(records) == 0:
    return
  
  # create webscraper and start scraping
  webscraper = Webscraper()
  try:
    for row in records:
      print(f"\nScraping for Alert {row[0]}...")
      webscraper.scrape(int(row[1]), int(row[2]), date.fromisoformat(row[3]), time.fromisoformat(row[4]), time.fromisoformat(row[5]))
  except OperationalError:
    print("Creating the `alerts` table...")
    Alert.createTable()
    print("Found 0 Alerts.")
  finally:
    webscraper.stop()
    
def listMode():
  try:
    records = CURSOR.execute("SELECT * FROM alerts").fetchall()
  except OperationalError:
    print("Creating the `alerts` table...")
    Alert.createTable()
    records = CURSOR.execute("SELECT * FROM alerts").fetchall()
  headers = ["ID", "Location", "Num Players", "Date", "Start Time", "End Time"]
  print(tabulate(records, headers, tablefmt="grid"))
    
if __name__ == "__main__":
  main()