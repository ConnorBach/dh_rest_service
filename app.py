import os
import json
import requests
from bs4 import BeautifulSoup
from flask import Flask

# South http://auxopsweb2.oit.nd.edu/DiningMenus/api/Menus/47
# North http://auxopsweb2.oit.nd.edu/DiningMenus/api/Menus/46

app = Flask(__name__)

url = 'https://dining.nd.edu/locations-menus/south-dining-hall/'
menuAPIurl = 'http://auxopsweb2.oit.nd.edu/DiningMenus/api/Menus/47'
response = requests.get(menuAPIurl) 
jsonRes = response.json()

'''
Building objects
Meal JSON Obj
{
    Start: '2018-07-25T06:30:00-04:00'
    End: '2018-07-25T09:00:00-04:00'
    Name: 'Breakfast'
    Menu: ['Apples', 'Bananas']
}
'''
Meals = []
curMeal = {}
curMeal['Menu'] = []
for meal in jsonRes:
    curMeal['Start'] = meal['EventStart']
    curMeal['End'] = meal['EventEnd']
    curMeal['Name'] = meal['Meal']
    for course in meal['Courses']:
        for menuItem in course['MenuItems']:
            curMeal['Menu'].append(menuItem['Name'])
    Meals.append(curMeal)
    curMeal = {}
    curMeal['Menu'] = []

[print(meal) for meal in Meals]


foods=[meal for meal in Meals]

@app.route("/")
def index():
    return "dh-rest-service"

@app.route("/api/foods")
def getFoods():
    return json.dumps(foods)

if __name__ == "__main__":
	app.run()