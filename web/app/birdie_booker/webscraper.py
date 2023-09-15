import os
import requests
from datetime import date, time, datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from ..webscraper import Webscraper
from .alert import get_alerts, set_expired_alert

class BirdieBookerWebscraper(Webscraper):
  def __init__(self):
    print("Initializing Birdie Booker webscraper...")
    super().__init__()
    
  def scrape(self):
    print("Starting Birdie Booker webscraper...\n")
    alerts = get_alerts()
    for alert in alerts:
      # if the current datetime is past an alert's datetime, set it as expired.
      # alert[0] = ID, alert[1] = locaiton ID, alert[3] = date, alert[5] = endTime, alert[6] = isExpired
      if alert[6] == 0 and datetime.strptime(alert[3], "%a %m/%d/%Y").date() < datetime.today().date():
        set_expired_alert(alert[0])
      else:
        if alert[1] == 0:
          date_formatted = datetime.strptime(alert[3], "%a %m/%d/%Y").strftime("%Y-%m-%d")
          self.recreation_park_18_scraper(alert[2], date_formatted, alert[4], alert[5])
      
  def recreation_park_18_scraper(self, numPlayers, date, startTime, endTime):
    print('Starting Recreation Park 18 web scraper...')
    url = f'https://letsgo.golf/recreation-park-golf-course-18/teeTimes/recreation-park-golf-course-18-california?date={date}&qty={numPlayers}'
    print(url)
    locationName = 'Recreation Park Golf Course 18'
    try:
      self.driver.get(url)
      print(self.driver.page_source)
      result = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".reservation-group-item")))
      events = self.driver.find_elements(By.CSS_SELECTOR, ".reservation-group-item")
    except TimeoutException as err:
      print(f"Waiting for presence of .reservation-group-item timed out. The element may not exist on the page.")
      print(err)
      return
    except Exception as err:
      print(err)
      return
    
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
      if eventTime > endTime:
        print(f"No events in range on date {date}")
        break
      elif eventTime > startTime and eventTime < endTime:
        print(f"Found event for {locationName} on {date} @ {eventTime}.")
        message = f"A booking is available at {locationName} on {date.strftime('%a %m/%d/%Y')} @ {time.strftime('%I:%M %p')}!"
        url_title = "Book now!"
        self.send_notif(message, url, url_title)
        break 
      print()