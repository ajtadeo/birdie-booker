from flask import Flask, render_template
from .birdie_booker.views import birdie_booker
import os

# initialize app
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

@app.route('/')
def home():
	return render_template("home.html")

app.register_blueprint(birdie_booker, url_prefix='/birdie-booker')