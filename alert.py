from datetime import date, time
import itertools
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

class Alert:
  id_iter = itertools.count() # used to create incremental ID's
  
  # def __init__(self):
  #   """ used for production only """
  #   self.id = next(self.id_iter)
  #   self.setSettings()
  
  def __init__(self, location, numPlayers, date, startTime, endTime):
    """ used for development/testing only """
    self.location = location
    self.numPlayers = numPlayers
    self.date = date
    self.startTime = startTime
    self.endTime = endTime
  
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
        self.date = date.fromisoformat(input("Enter the booking date (YYYY-MM-DD): "))
        if self.date < date.today():
          raise ValueError
      except ValueError:
        print("\nSorry, date was invalid or in an invalid format.")
        continue
      else:
        break
      
    # get start time
    while True:
      try:
        self.startTime = time.fromisoformat(input("Enter start time (HH:MM, 24hr): "))
      except ValueError:
        print("\nSorry, start time was invalid or in an invalid format.")
        continue
      else:
        break
      
      # get end time
    while True:
      try:
        self.endTime = time.fromisoformat(input("Enter end time (HH:MM, 24hr): "))
        if self.endTime < self.startTime:
          raise ValueError
      except ValueError:
        print("\nSorry, end time was before start time or in an invalid format.")
        continue
      else:
        break
      
    # confirm settings
    confirmMsg = f"""
-------------------
Alert ID:\t\t{self.id}

Location:\t{Location(self.location).name}
Players:\t{self.numPlayers}
Date:\t\t{self.date}
Start Time:\t{self.startTime}
End Time:\t{self.endTime}
-------------------
Confirm these settings? (y/n): """
    result = input(confirmMsg)
    while result != "n" and result != "y":
      print("\nSorry, that input is invalid.")
      result = input(confirmMsg)
    if result.lower() == "n":
      updateSettings()
      
  def getSettings(self):
    msg = f"""
-------------------
ID:\t\t{self.id}

Location:\t{self.location}
Players:\t{self.numPlayers}
Date:\t\t{self.date}
Start Time:\t{self.startTime}
End Time:\t{self.endTime}
-------------------
    """
    print(msg)
    
  def scrape(self):
    if self.location == 0:
      self.recreationPark18_scraper()
    
  def recreationPark18_scraper(self):
    """ Scrapes Recreation Park 18 website and sends a notification if an alert exists """
    url = f'https://letsgo.golf/recreation-park-golf-course-18/teeTimes/recreation-park-golf-course-18-california?date={self.date}&qty={self.numPlayers}'
    name = 'Recreation Park Golf Course 18'
        
    print('Starting Recreation Park 18 web scraper...')
    try:
      # set up options
      options = Options()
      options.add_argument('--headless=new')
      options.add_argument("--disable-gpu")
      options.add_argument('--blink-settings=imagesEnabled=false')

      # set up driver
      driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
      driver.get(url)

      # wait for page to load, then scrape all available events
      try:
        WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, ".reservation-group-item"))
        )
      except TimeoutException:
        print(f"No events exist on date {self.date}")
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
        if eventTime > self.startTime and eventTime < self.endTime:
          print(f"Found event at {eventTime.strftime('%I:%M %p')}. Sending a notification to PushSafer...")
          sendMessage(name, eventTime.strftime('%I:%M %p'), url)
          break 
        
    except Exception as err:
      print(err)

    print("Done.")
    
def sendMessage(location, time, bookingURL):
  url = 'https://www.pushsafer.com/api'
  params = {
    "t": "Birdie Booker",
    "m": f"A booking is available at {location} @ {time}!",
    "v": 1,
    "u" : bookingURL,
    "ut" : 'Book Now',
    "k": os.environ.get("PRIVATE_KEY")
  }

  try:
    r = requests.get(url, params=params)
    r.raise_for_status()
    print(r.json())
  except requests.exceptions.RequestException as e:
    raise SystemExit(e)