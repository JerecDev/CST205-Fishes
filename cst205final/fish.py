from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import json

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fish', methods=['GET', 'post'])
def fish():
    req = requests.get('https://www.fishwatch.gov/api/species')
    data = json.loads(req.content)
    #data = req.content
    return render_template('fish.html', data=data)

   

