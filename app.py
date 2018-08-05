import os
import json
import requests
import psycopg2
from datetime import datetime
from bs4 import BeautifulSoup
from flask import Flask

# South http://auxopsweb2.oit.nd.edu/DiningMenus/api/Menus/47
# North http://auxopsweb2.oit.nd.edu/DiningMenus/api/Menus/46

app = Flask(__name__)
DATABASE_URL = os.environ['DATABASE_URL']

url = 'https://dining.nd.edu/locations-menus/south-dining-hall/'
menuAPIurl = 'http://auxopsweb2.oit.nd.edu/DiningMenus/api/Menus/47'
Meals = []

@app.before_request
def loadData():
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
    # Meals = []
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

    # [print(meal) for meal in Meals]


    foods=[meal['Menu'] for meal in Meals]
    conn = None
    try: 
        conn = psycopg2.connect(database=DATABASE_URL, sslmode='require')

        for menu in foods:
            for food in menu:
                # check if in database, add if not
                cur = conn.cursor()
                cur.execute('SELECT foods.name FROM foods WHERE foods.name = \'{0}\''.format(food.replace('\'', '')))

                if not cur.fetchone():
                    print('insert', food)
                    cur.execute('INSERT INTO foods VALUES (\'{0}\')'.format(food.replace('\'', '')))
                
                cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()

@app.route("/")
def index():
    return "dh-rest-service"

@app.route("/api/today")
def getToday():
    today = datetime.utcnow() 
    todayMeals = []
    for meal in Meals:
        mealDate = meal['Start'].split('T')[0]
        temp = mealDate.split('-')
        years = int(temp[0])
        months = int(temp[1])
        days = int(temp[2])
        if years == today.year and months == today.month and days == today.day:
            todayMeals.append(meal)
    return json.dumps(todayMeals)

@app.route("/api/everyFood")
def everyFood():
    try:
        conn = psycopg2.connect(database=DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute('SELECT * FROM foods')
        rows = cur.fetchall()
        return json.dumps(rows)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()
    return "Error grabbing foods from database"


if __name__ == "__main__":
	app.run()