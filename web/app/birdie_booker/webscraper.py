import os
import requests
from datetime import date, time, datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from app.webscraper import Webscraper
from app.birdie_booker.alert import get_alerts, set_expired_alert
from app.birdie_booker.location import get_locations

class BirdieBookerWebscraper(Webscraper):
  def __init__(self):
    print("Initializing Birdie Booker webscraper...")
    self.locations = get_locations()
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
        # convert date, startTime, and endTime to datetime objects for scraping functions
        date = datetime.strptime(alert[3], "%a %m/%d/%Y")
        startTime = datetime.strptime(alert[4], "%I:%M %p").time()
        endTime = datetime.strptime(alert[5], "%I:%M %p").time()
        
        if alert[1] == 1:
          self.recreation_park_18_scraper(alert[2], date, startTime, endTime)
        elif alert[1] == 2:
          self.golfLink_scraper(
            alert[2], date, startTime, endTime,
            "https://www.golflink.com/golf-courses/ca/long-beach/el-dorado-park-golf-course-66634/rates-tee-times",
            "El Dorado Park Golf Course"
          )
        elif alert[1] == 3:
          self.golfLink_scraper(
            alert[2], date, startTime, endTime,
            "https://www.golflink.com/golf-courses/ca/cypress/navy-golf-course-87734/rates-tee-times", 
            "Navy Golf Course Cypress, Cruiser Course"
          )
        elif alert[1] == 4:
          self.golfLink_scraper(
            alert[2], date, startTime, endTime, 
            "https://www.golflink.com/golf-courses/ca/cypress/navy-golf-course-87634/rates-tee-times", 
            "Navy Golf Course Cypress, Destroyer Course"
          )
      
  # currently unavailable because of Cloudflare </3
  def recreation_park_18_scraper(self, numPlayers, date, startTime, endTime):
    print('Starting Recreation Park 18 web scraper...')
    url = f'https://letsgo.golf/recreation-park-golf-course-18/teeTimes/recreation-park-golf-course-18-california?date={date.strftime("%Y-%m-%d")}&qty={numPlayers}'
    print(url)
    locationName = 'Recreation Park Golf Course 18'
    try:
      self.driver.get(url)
      self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".reservation-group-item")))
      events = self.driver.find_elements(By.CSS_SELECTOR, ".reservation-group-item")
    except TimeoutException as err:
      print(f"Waiting for presence of .reservation-group-item timed out. The element may not exist on the page.")
      print(err)
      return
    except Exception as err:
      print(err)
      return
    
    for event in events:
      eventTimeRaw = event.find_element(By.CSS_SELECTOR, ".start-time").text
      eventTime = datetime.strptime(eventTimeRaw, "%I:%M %p").time()
      
      if eventTime > endTime:
        print(f"No events in range on date {date}")
        break
      elif eventTime > startTime and eventTime < endTime:
        print(f"Found event for {locationName} on {date} @ {eventTime}.")
        message = f"A booking is available at {locationName} on {date.strftime('%a %m/%d/%Y')} @ {time.strftime('%I:%M %p')}!"
        url_title = "Book now!"
        self.send_notif(message, url, url_title)
        break 
      
  def golfLink_scraper(self, numPlayers, date, startTime, endTime, base_url, locationName):
    url = base_url + f"?from_date={date.strftime('%m-%d-%Y')}&to_date={date.strftime('%m-%d-%Y')}&tee_time_min={startTime.hour}&tee_time_max={endTime.hour}&min_price=0&max_price=500&players_min={numPlayers}&holes=0&AID=&FID=9834&lat=0&lon=0&action=search&sort_by=Time%7Casc"
    try:
      self.driver.get(url)
      result = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".tee-time")))
      events = result.find_elements(By.CSS_SELECTOR, ".main-info")
    except TimeoutException as err:
      print(f"Waiting for presence of .tee-time timed out. No events detected.")
      return
    except Exception as err:
      print(err)
      return
    
    # send a notification if an event lies in the set time period
    for event in events:
      eventTimeRaw = event.find_element(By.CSS_SELECTOR, ".time a").text
      eventTime = datetime.strptime(eventTimeRaw, "%A, %B %d, %Y %I:%M %p").time()
      
      if eventTime > endTime:
        print(f"No events in range on date {date}")
        break
      elif eventTime > startTime and eventTime < endTime:
        print(f"Found event for {locationName} on {date} @ {eventTime}.")
        message = f"A booking is available at {locationName} on {date.strftime('%a %m/%d/%Y')} @ {eventTime.strftime('%I:%M %p')}!"
        url_title = "Book now!"
        self.send_notif(message, url, url_title)
        break 