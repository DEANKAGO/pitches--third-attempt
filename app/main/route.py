from flask import render_template, url_for, Blueprint

main= Blueprint('main',__name__)

@main.route('/')
def home():
    # All pitches here
  pass

