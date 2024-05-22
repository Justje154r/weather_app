from flask import Flask, render_template, request, url_for
import requests
from config import API_KEY

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather_data = get_weather(city)
    return render_template('index.html', weather=weather_data)

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        weather = response.json()
        weather_icon = get_weather_icon(weather['weather'][0]['main'])
        weather['icon_url'] = url_for('static', filename=f'img/{weather_icon}')
        return weather
    else:
        return None

def get_weather_icon(weather_condition):
    icons = {
        'Clear': 'sunny.png',
        'Clouds': 'cloudy.png',
        'Rain': 'rainy.png',
        'Snow': 'snowy.png',
        'Thunderstorm': 'stormy.png'
    }
    return icons.get(weather_condition, 'unknown.png')

if __name__ == '__main__':
    app.run(debug=True)