from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config, API_KEY
from models import db, User, Favorite
import requests

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather_data = get_weather(city)
    return render_template('index.html', weather=weather_data, is_premium=current_user.is_authenticated and current_user.is_premium)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        is_premium = request.form.get('is_premium') == 'on'
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
        else:
            user = User(username=username, email=email, password_hash=generate_password_hash(password), is_premium=is_premium)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/favorites', methods=['GET', 'POST'])
@login_required
def favorites():
    if request.method == 'POST':
        city = request.form.get('city')
        country = request.form.get('country')
        if city and country:
            favorite = Favorite(city=city, country=country, user_id=current_user.id)
            db.session.add(favorite)
            db.session.commit()
            flash('Favorite added successfully')
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('favorites.html', favorites=favorites)

@app.route('/delete_favorite/<int:id>')
@login_required
def delete_favorite(id):
    favorite = Favorite.query.get(id)
    if favorite and favorite.user_id == current_user.id:
        db.session.delete(favorite)
        db.session.commit()
        flash('Favorite deleted successfully')
    return redirect(url_for('favorites'))

@app.route('/map')
@login_required
def map():
    return render_template('map.html')

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
    with app.app_context():
        db.create_all()
    app.run(debug=True)