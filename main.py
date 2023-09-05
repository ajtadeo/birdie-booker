#!/usr/bin/env python3
from pushsafer import Client
import os
import requests
from dotenv import load_dotenv

load_dotenv()

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

sendMessage("Heartwell Golf Course", 'https://foreupsoftware.com/index.php/booking/20172/3881#teetimes')