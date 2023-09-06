#!/usr/bin/env python3
from pushsafer import Client
import os
import requests
from dotenv import load_dotenv
from alert import Alert
from location import Location
import datetime

load_dotenv()

def main():
  print("Welcome to Birdie Booker!\n")
  alert1 = Alert(0, 3, datetime.date.fromisoformat("2023-09-07"), datetime.time.fromisoformat("12:00"), datetime.time.fromisoformat("14:00"))
  alert1.scrape()
  
if __name__ == "__main__":
  main()