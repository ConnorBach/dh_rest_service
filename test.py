import requests

r = requests.get("https://dining.nd.edu/locations-menus/south-dining-hall/")
print(r.text)
