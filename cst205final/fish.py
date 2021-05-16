from flask import Flask, render_template, flash, redirect
from werkzeug.utils import validate_arguments
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests, json, html
from random import choices
print(" ### program start")
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'csumb-otter'

# Moved request to outside functions to load faster
r = requests.get('https://www.fishwatch.gov/api/species')
data = r.json()

# class for search form in fish.html
class Search(FlaskForm):
    name = StringField(
        'Name', 
        validators=[DataRequired()]
    )

# Home page for the application
# Created by Angelo Ediriweera, Zachary Abbett, Elijah Barsky-Ex, and Ryan Gutierrez
@app.route('/')
def index():
    return render_template('index.html')

# Routes to about.html which displays sources used in application and information about the creators of the application
# Created by 
@app.route('/about')
def about():
    return render_template('about.html')

# Route function to render fish.html, which serves as a hub for users to search and view information about various fish species
# Created By Ryan Gutierrez and Angelo Ediriweera
@app.route('/fish/<tbSize>', methods=['GET', 'POST'])
def fish(tbSize):
    print(" ### fish")
    randList = choices(data, k=int(tbSize))
    # Uses Scientific name from the users entry to find a macthing dict in data
    form = Search()
    if form.is_submitted():
        print("submitted")
    if form.validate():
        print("valid")
    print(form.errors)
    if form.validate_on_submit():
        print(" ### form validated")
        return redirect('/fishInfo/'+str(form.name.data))

    return render_template('fish.html', data=data, randList=randList, form=form)

# Route function to render fishInfo.html, which displays specific information about a fish the user chose in fish.html
# Will default to White Hake (first entry in data) if the users input does not match any item['Species Name'] in data
# Created by Ryan Gutierrez
@app.route('/fishInfo/<sciName>')
def fishInfo(sciName):
    print(" ### fishInfo")
    fishData = data[0]
    for item in data:
            if(item['Species Name'] == sciName):
                fishData = item
    img = fishData['Species Illustration Photo']
    # Remove all html tags from the elements of fishData that are of type str
    for key in fishData.keys():
        if(type(fishData[key])==str):
            fishData[key] = removeTags(fishData[key])

    return render_template('fishInfo.html', fishData=fishData, img=img)

# Helper function given a string s will return a 'clean' string with no html tags or entities.
# If s does not contain html tags or entites then the string will be unaffected.
# Created by Ryan Gutierrez
def removeTags(s):
    import re
    # Removes entities
    s = html.unescape(s)
    # Removes Tags
    clean = re.compile('<.*?>')
    # Return clean string
    return re.sub(clean, '', str(s))




# Keys in individual fish dict:
#     'Fishery Management', 
#     'Habitat', 
#     'Habitat Impacts', 
#     'Image Gallery', 
#     'Location', 
#     'Management', 
#     'NOAA Fisheries Region', 
#     'Population', 
#     'Population Status', 
#     'Scientific Name', 
#     'Species Aliases', 
#     'Species Illustration Photo', 
#     'Species Name', 
#     'Animal Health', 
#     'Availability', 
#     'Biology', 
#     'Bycatch', 
#     'Calories', 
#     'Carbohydrate', 
#     'Cholesterol', 
#     'Color', 
#     'Disease Treatment and Prevention', 
#     'Diseases in Salmon', 
#     'Displayed Seafood Profile Illustration', 
#     'Ecosystem Services', 
#     'Environmental Considerations', 
#     'Environmental Effects', 
#     'Farming Methods', 
#     'Farming Methods_', 
#     'Fat, Total', 
#     'Feeds_', 
#     'Feeds', 
#     'Fiber, Total Dietary', 
#     'Fishing Rate', 
#     'Harvest', 
#     'Harvest Type', 
#     'Health Benefits', 
#     'Human_Health_', 
#     'Human Health', 
#     'Physical Description', 
#     'Production', 
#     'Protein', 
#     'Quote', 
#     'Quote Background Color', 
#     'Research', 
#     'Saturated Fatty Acids, Total', 
#     'Selenium', 
#     'Serving Weight', 
#     'Servings', 
#     'Sodium', 
#     'Source', 
#     'Sugars, Total', 
#     'Taste', 
#     'Texture', 
#     'Path', 
#     'last_update'