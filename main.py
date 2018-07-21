import os
import json
from selenium import webdriver
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)

url = 'https://dining.nd.edu/locations-menus/south-dining-hall/'
web = webdriver.Chrome("/Applications/chromedriver")
web.get(url)
html = web.page_source
print(html)
web.quit()

soup = BeautifulSoup(html)
menu = soup.find('div', {'class' : 'menu-container'})
print(menu)

spans = soup.find_all('span', {'class' : 'menu-item-name'})
foods = [span.get_text() for span in spans]

print(foods)

@app.route("/api/foods")
def getFoods():
    return json.dumps(foods)