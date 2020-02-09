from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import json
import requests
from bson import json_util


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/flask-weather"
mongo = PyMongo(app)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    weather_data = []
    name_city = ''
    if request.method == 'POST':
        name_city = request.form['city']
        add_city = mongo.db.cities.insert_one({'name': name_city})


    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    cities = mongo.db.cities.find()
    

    for city in cities:
            r = requests.get(url.format(city['name'])).json()

            weather = {
                'city' : city['name'],
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
            }

            weather_data.append(weather)


    return render_template('weather.html', weather_data=weather_data)

if __name__ == '__main__':
   app.run(debug=True)