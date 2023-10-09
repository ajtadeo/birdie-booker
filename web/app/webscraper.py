import os
import requests

# import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

class Webscraper:
  """ 
  This is the base Webscraper class which hosts an instance of Chromedriver for all scraping tasks.
  """
  def __init__(self):
    print("Initializing webscraper...")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument("--disable-gpu")
    options.add_argument('--blink-settings=imagesEnabled=false')

    # services in a docker network are accessible by http://<service name>:<port>
    self.driver = webdriver.Remote(
      command_executor=f'http://selenium:4444/wd/hub', 
      options=options
    )
    self.wait = WebDriverWait(self.driver, 10)
    
  def __del__(self):
    try:
      self.driver.quit()
    except AttributeError:
      print("Webscraper failed to build.")
    
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