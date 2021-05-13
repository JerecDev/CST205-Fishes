from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import json
from random import choices

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Moved request to outside functions to load faster
r = requests.get('https://www.fishwatch.gov/api/species')
data = r.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fish/<tbSize>', methods=['GET', 'post'])
def fish(tbSize):
    randList = choices(data, k=int(tbSize))
    #data = req.content
    return render_template('fish.html', data=data, randList=randList)
    