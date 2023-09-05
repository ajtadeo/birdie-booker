#!/usr/bin/env python3
from pushsafer import Client
import os
import requests
from dotenv import load_dotenv
from datetime import date

load_dotenv()

PLAYERS = 0
DATE = date.today()

def main():
  print("Welcome to Birdie Booker!\n")
  updateSettings()
  print("Starting web scrapers...")
    
def updateSettings():  
  # get number of players
  while True:
    global PLAYERS
    try:
      PLAYERS = int(input("Enter the number of players: "))
      if PLAYERS < 1 or PLAYERS > 4:
        raise ValueError
    except ValueError:
      print("\nSorry, player number must an integer between 1 and 4.")
      continue
    else:
      break
    
  # get date
  while True:
    global DATE
    try:
      DATE = date.fromisoformat(input("Enter the booking date (YYYY-MM-DD): "))
      if DATE < date.today():
        raise ValueError
    except ValueError:
      print("\nSorry, date was invalid or in an invalid format.")
      continue
    else:
      break
    
  # confirm settings
  confirmMsg = f"-------------------\n\tPlayers: {PLAYERS}\n\tDate: {DATE}\n-------------------\nConfirm these settings? (y/n): "
  result = input(confirmMsg)
  while result != "n" and result != "y":
    print("\nSorry, that input is invalid.")
    result = input(confirmMsg)
  if result.lower() == "n":
    updateSettings()

def sendMessage(location, bookingURL):
  url = 'https://www.pushsafer.com/api'
  params = {
    "t": "Birdie Booker",
    "m": f"A booking is available at {location}!",
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

def recreationPark18_scraper():
  url = 'https://foreupsoftware.com/index.php/booking/20172/3881#teetimes'
  location = 'Recreation Park 18'
  sendMessage(location, url)
  
if __name__ == "__main__":
  main()