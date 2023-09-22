import os
import requests

import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service

class Webscraper:
  """ 
  This is the base Webscraper class which hosts an instance of Undetected Chromedriver for all scraping tasks.
  
    * Undetected Chrome Driver: major version 117
    * Chrome Binary: major version 117
  """
  def __init__(self):
    options = uc.ChromeOptions()
    options.binary_location = os.environ.get("CHROME_BINARY_PATH")
    options.add_argument('--headless=new')
    options.add_argument("--disable-gpu")
    options.add_argument('--blink-settings=imagesEnabled=false')

    self.driver = uc.Chrome(service=Service(executable_path=os.environ.get("CHROMEDRIVER_PATH")), options=options, version_main=117)
    self.wait = WebDriverWait(self.driver, 10)
    
  def __del__(self):
    self.driver.quit()
    
  def scrape(self):
    pass
  
  def send_notif(self, message, url, url_title):
    print("Sending a Pushover notification...")
    pushover_url = 'https://api.pushover.net/1/messages.json'
    params = {
      "token": os.environ.get("PUSHOVER_API_KEY"),
      "user": os.environ.get("PUSHOVER_USER_KEY"),
      "message": message,
      "url" : url,
      "url_title" : url_title,
      "priority": 1
    }

    try:
      r = requests.post(pushover_url, params=params)
      r.raise_for_status()
      print(r.json())
    except requests.exceptions.RequestException as e:
      raise SystemExit(e)
    print("Done.")