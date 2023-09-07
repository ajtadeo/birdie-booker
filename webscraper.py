import os
import requests
from datetime import date, time

# selenium/chrome driver
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class Webscraper:
  def __init__(self):
    print("Setting up Chrome Driver...")
    
    # set up options
    options = uc.ChromeOptions()
    options.binary_location = "/Users/ajtadeo/chromedriver-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
    options.add_argument('--headless=new')
    options.add_argument("--disable-gpu")
    options.add_argument('--blink-settings=imagesEnabled=false')

    # set up driver
    self.driver = uc.Chrome(service=Service(executable_path='/Users/ajtadeo/chromedriver-mac-x64/chromedriver'), options=options)
    
    # set up webdriverwait
    self.wait = WebDriverWait(self.driver, 5)
    
  def stop(self):
    print("Stopping web scraper...")
    self.driver.quit()
    
  def scrape(self, location, numPlayers, date, startTime, endTime):
    if location == 0:
      self.recreationPark18_scraper(numPlayers, date, startTime, endTime)
    
  def sendNotif(self, locationName, date, time, bookingURL):
    url = 'https://api.pushover.net/1/messages.json'
    params = {
      "token": os.environ.get("PUSHOVER_API_KEY"),
      "user": os.environ.get("PUSHOVER_GROUP_KEY"),
      "message": f"A booking is available at {locationName} on {date.strftime('%B %d, %Y')} @ {time.strftime('%I:%M %p')}!",
      "url" : bookingURL,
      "url_title" : 'Book Now',
    }

    try:
      r = requests.post(url, params=params)
      r.raise_for_status()
      print(r.json())
    except requests.exceptions.RequestException as e:
      raise SystemExit(e)
      
  def recreationPark18_scraper(self, numPlayers, date, startTime, endTime):
    """ Scrapes Recreation Park 18 website and sends a notification if an alert exists """
    url = f'https://letsgo.golf/recreation-park-golf-course-18/teeTimes/recreation-park-golf-course-18-california?date={date}&qty={numPlayers}'
    locationName = 'Recreation Park Golf Course 18'
        
    print('Starting Recreation Park 18 web scraper...')
    try:
      self.driver.get(url)
      try:
        result = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".reservation-group-item")))
      except TimeoutException as err:
        print(f"No events found on date {date}")
        return
      except Exception as err:
        print(err)
        return
      
      events = self.driver.find_elements(By.CSS_SELECTOR, ".reservation-group-item")
      
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
          print(f"Found event on {date} @ {eventTime}. Sending a notification to PushOver...")
          self.sendNotif(locationName, date, eventTime, url)
          break 
        
    except Exception as err:
      print(err)