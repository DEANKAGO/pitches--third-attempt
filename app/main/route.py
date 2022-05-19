from flask import render_template, url_for, Blueprint
from app.models import Notice,Complaints
main= Blueprint('main',__name__)

@main.route('/')
def home():
    # All pitches here

  return render_template('home.html')





