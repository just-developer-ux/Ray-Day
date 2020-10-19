import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecret'
merk = 1.333

def get_current_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={ city }&units=metric&lang=ru&appid=6508b903fa6ea03d764bfe659fe6c985'
    r = requests.get(url).json()
    return r

def get_forecast_5_days(city):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={ city }&units=metric&lang=ru&appid=6508b903fa6ea03d764bfe659fe6c985'
    t = requests.get(url).json()
    return t


@app.route('/', methods=["POST", "GET"])
def home_page():
    if request.method == "POST":
        city = request.form["city"]
        return redirect("/погода-у-"+city)

    return render_template('home.html')


@app.route("/погода-у-<city>", methods=["POST", "GET"])
def index(city):
    
    if request.method == "GET":
        r = get_current_weather_data(city)
        t = get_forecast_5_days(city)

        if r['cod'] == 200:
            current_weather_data = []
            forecast_5_days_data = []

            b = r['main']['temp']
            if b > 30:
                gradient = "0deg, rgb(255,0,0), rgb(0,255,0), rgb(0,0,255)"
            else:
                gradient = "0deg, rgb(0,0,255), rgb(0,255,0), rgb(255,0,0)"


            weather = {
                    'name' : city,
                    'temperature' : r['main']['temp'],
                    'description' : r['weather'][0]['description'],
                    'icon' : r['weather'][0]['icon'],
                    'pressure' : round(r['main']['pressure'] / merk),
                    'humidity' : r['main']['humidity'],
                    'visibility' : r['visibility'],
                    'wind_speed' : r['wind']['speed'],
                    'wind_deg' : r['wind']['deg'],
                    'clouds' : r['clouds']['all'],
                    'city_id' : r['id'],
                    'gradient' : gradient,
                }
            
            i = 0
            length = len(t.get('list'))

            while i < length:
                n = t['list'][i]['main']['temp']

                if n > 30:
                    gradient = "0deg, rgb(255,0,0), rgb(0,255,0), rgb(0,0,255)"
                else:
                    gradient = "0deg, rgb(0,0,255), rgb(0,255,0), rgb(255,0,0)"

                forecast = {
                        'temperature' : t['list'][i]['main']['temp'],
                        'description' : t['list'][i]['weather'][0]['description'],
                        'icon' : t['list'][i]['weather'][0]['icon'],
                        'pressure' : round(t['list'][i]['main']['pressure'] / merk),
                        'humidity' : t['list'][i]['main']['humidity'],
                        'visibility' : t['list'][i]['visibility'],
                        'wind_speed' : t['list'][i]['wind']['speed'],
                        'wind_deg' : t['list'][i]['wind']['deg'],
                        'clouds' : t['list'][i]['clouds']['all'],
                        'time' : t['list'][i]['dt_txt'],
                        'gradient' : gradient,
                    }
                forecast_5_days_data.append(forecast)
                i+=8
                        
            current_weather_data.append(weather)
            

            return render_template('weather.html', weather_data=current_weather_data, forecast_5_days=forecast_5_days_data, city_name=city)

        else:
            flash("Даного населеного пункту не існує, або його назва неправильно вказана")
            return redirect("/")
            

    else:
        city = request.form['city']

        r = get_current_weather_data(city)
        t = get_forecast_5_days(city)
        
        if r['cod'] == 200:
            current_weather_data = []
            forecast_5_days_data = []

            b = r['main']['temp']
            if b > 30:
                gradient = "0deg, rgb(255,0,0), rgb(0,255,0), rgb(0,0,255)"
            else:
                gradient = "0deg, rgb(0,0,255), rgb(0,255,0), rgb(255,0,0)"


            weather = {
                    'name' : city,
                    'temperature' : r['main']['temp'],
                    'description' : r['weather'][0]['description'],
                    'icon' : r['weather'][0]['icon'],
                    'pressure' : round(r['main']['pressure'] / merk),
                    'humidity' : r['main']['humidity'],
                    'visibility' : r['visibility'],
                    'wind_speed' : r['wind']['speed'],
                    'wind_deg' : r['wind']['deg'],
                    'clouds' : r['clouds']['all'],
                    'city_id' : r['id'],
                    'gradient' : gradient,
                }

            i = 0
            length = len(t.get('list'))
            while i < length:
                forecast = {
                        'temperature' : t['list'][i]['main']['temp'],
                        'description' : t['list'][i]['weather'][0]['description'],
                        'icon' : t['list'][i]['weather'][0]['icon'],
                        'pressure' : round(t['list'][i]['main']['pressure'] / merk),
                        'humidity' : t['list'][i]['main']['humidity'],
                        'visibility' : t['list'][i]['visibility'],
                        'wind_speed' : t['list'][i]['wind']['speed'],
                        'wind_deg' : t['list'][i]['wind']['deg'],
                        'clouds' : t['list'][i]['clouds']['all'],
                        'time' : t['list'][i]['dt_txt'],     
                    }
                forecast_5_days_data.append(forecast)
                i+=8

            current_weather_data.append(weather)

            return render_template('weather.html', weather_data=current_weather_data, forecast_5_days=forecast_5_days_data, city_name=city)

        else:
            flash("Даного населеного пункту не існує, або його назва неправильно вказана")
            return redirect("/")

@app.route("/news")
def news():
    pass

@app.route("/exchange-rate")
def mon():
    pass

@app.route("/holydays")
def holyd():
    pass

if __name__ == "__main__":
    app.run()
