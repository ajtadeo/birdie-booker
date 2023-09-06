from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# set up options
options = Options()
options.binary_location = "/Users/ajtadeo/chromedriver-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
options.add_argument('--headless=new')
options.add_argument("--disable-gpu")
options.add_argument('--blink-settings=imagesEnabled=false')

# set up driver
driver = webdriver.Chrome(service=Service(executable_path='/Users/ajtadeo/chromedriver-mac-x64/chromedriver'), options=options)