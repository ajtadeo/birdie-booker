#!/usr/bin/env python3
from dotenv import load_dotenv
from alert import Alert
from datetime import date, time, datetime
import argparse
from db import CONN, CURSOR
from tabulate import tabulate
from sqlite3 import OperationalError
import os
import requests
from driver import driver

# selenium/chrome driver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

# TODO: set CRON job for every 5 minutes

def main():
  parser = argparse.ArgumentParser()
  mode = parser.add_mutually_exclusive_group()
  mode.add_argument("-s", "--scrape", dest="scrape", action="store_true", help="Running web scrapers for Alerts")
  mode.add_argument("-l", "--list", dest="list", action="store_true", help="List existing Alerts")
  args = parser.parse_args()
  
  if args.scrape:
    try:
      print(f"Starting script at: {datetime.now()}\n\n")
      print("Scraping existing Alerts...")
      records = CURSOR.execute("SELECT * FROM alerts").fetchall()
      headers = ["ID", "Location", "Num Players", "Date", "Start Time", "End Time"]
      print(tabulate(records, headers, tablefmt="grid"))
      if len(records) == 0:
        return
      for row in records:
        print(f"Scraping for Alert {row[0]}...")
        # location, numPlayers, date, startTime, endTime
        scrape(int(row[1]), int(row[2]), date.fromisoformat(row[3]), time.fromisoformat(row[4]), time.fromisoformat(row[5]))
    except OperationalError:
      print("Creating the `alerts` table...")
      Alert.createTable()
      print("Found 0 Alerts.")
  elif args.list:
    try:
      records = CURSOR.execute("SELECT * FROM alerts").fetchall()
    except OperationalError:
      print("Creating the `alerts` table...")
      Alert.createTable()
      records = CURSOR.execute("SELECT * FROM alerts").fetchall()
    headers = ["ID", "Location", "Num Players", "Date", "Start Time", "End Time"]
    print(tabulate(records, headers, tablefmt="grid"))
  else:
    try:
      print("Creating an Alert...")
      myAlert = Alert()
      myAlert.save()
    except Exception as e:
      print(e)
    
def scrape(location, numPlayers, date, startTime, endTime):
  if location == 0:
    recreationPark18_scraper(numPlayers, date, startTime, endTime)
  
def recreationPark18_scraper(numPlayers, date, startTime, endTime):
  """ Scrapes Recreation Park 18 website and sends a notification if an alert exists """
  url = f'https://letsgo.golf/recreation-park-golf-course-18/teeTimes/recreation-park-golf-course-18-california?date={date}&qty={numPlayers}'
  name = 'Recreation Park Golf Course 18'
      
  print('Starting Recreation Park 18 web scraper...')
  try:
    driver.get(url)
    try:
      WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".reservation-group-item"))
      )
    except TimeoutException:
      print(f"No events exist on date {date}")
      return
    
    events = driver.find_elements(By.CSS_SELECTOR, ".reservation-group-item")
    
    # send a notification if an event lies in the set time period
    for event in events:
      eventTimeList = list(event.find_element(By.CSS_SELECTOR, ".start-time").text.split(":"))
      hour = int(eventTimeList[0])
      meridian = eventTimeList[1][3:]
      minute = eventTimeList[1][:2]
      if hour == 12:
        hour = 0
      if meridian == 'PM':
        hour += 12
      
      eventTime = time.fromisoformat(f"{hour}:{minute}")
      if eventTime > startTime and eventTime < endTime:
        print(f"Found event on {date.strftime('%B %d, %Y')} @ {eventTime.strftime('%I:%M %p')}. Sending a notification to PushOver...")
        sendMessage(name, date, eventTime, url)
        break 
      
  except Exception as err:
    print(err)

  print("Done.")
  
def sendMessage(location, date, time, bookingURL):
  url = 'https://api.pushover.net/1/messages.json'
  params = {
    "token": os.environ.get("PUSHOVER_API_KEY"),
    "user": os.environ.get("PUSHOVER_USER_KEY"),
    "message": f"A booking is available at {location} on {date.strftime('%B %d, %Y')} @ {time.strftime('%I:%M %p')}!",
    "url" : bookingURL,
    "url_title" : 'Book Now',
  }

  try:
    r = requests.post(url, params=params)
    r.raise_for_status()
    print(r.json())
  except requests.exceptions.RequestException as e:
    raise SystemExit(e)
    
if __name__ == "__main__":
  main()