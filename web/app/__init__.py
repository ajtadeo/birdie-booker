from flask import Flask, render_template
from flask_apscheduler import APScheduler
import os
from datetime import datetime

from .birdie_booker.views import birdie_booker
from .birdie_booker.webscraper import BirdieBookerWebscraper

from .webscraper import Webscraper

# initialize app
app = Flask(__name__)
app.config.from_mapping(
  SCHEDULER_API_ENABLED=True,
  SECRET_KEY=os.environ.get('SECRET_KEY')
)

# app routes
app.register_blueprint(birdie_booker, url_prefix='/birdie-booker')
@app.route('/')
def home():
	return render_template("home.html")

# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# initialize webscrapers
webscrapers = [
  BirdieBookerWebscraper()
]

@scheduler.task("cron", id="scrape", minute="*/5")
def scrape():
  print(f"Starting cron at {datetime.now(tz='PST')}...\n=======================\n")
  for w in webscrapers:
    w.scrape()
  print(f"\n=======================\nCron completed at {datetime.now()}.")