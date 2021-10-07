from datetime import datetime, timedelta
import configparser
import requests
from flask import Flask, render_template, request


app = Flask(__name__)


def get_location():
    try:
        response = requests.get(f'http://ip-api.com/json/')
        geo_data = response.json()
        city_name = geo_data['city']
        country_code = geo_data['countryCode']
        return city_name + ', ' + country_code
    except:
        return 'Jerusalem'


@app.route('/', methods=['GET', 'POST'])
def home():
    config = configparser.ConfigParser()
    config.read('config.ini')
    API_KEY = config['openweathermap']['api']
    # If there is no city name provided, get user's location and display that city weather:
    if request.method == 'POST':
        city_name = request.form['city-name']
    else:
        city_name = get_location()
    daily_source = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={API_KEY}'
    daily_data = requests.get(daily_source).json()
    print(daily_data)
    now = datetime.now()  # current date and time
    date_time = now.strftime("%d/%m/%Y, %H:%M")

    class DailyWeather:
        city = daily_data['name']
        country = daily_data['sys']['country']
        temp = "{:.1f}".format(int(daily_data['main']['temp']))
        temp_feels = "{:.1f}".format(int(daily_data['main']['feels_like']))
        wind = "{:.1f}".format(daily_data['wind']['speed'] * 3.6)
        humidity = daily_data['main']['humidity']
        temp_max = "{:.1f}".format(int(daily_data['main']['temp_max']))
        temp_min = "{:.1f}".format(int(daily_data['main']['temp_min']))
        city_lon = daily_data['coord']['lon']
        city_lat = daily_data['coord']['lat']
        datetime_get = daily_data['dt']
        short_desc = daily_data['weather'][0]['main']
        desc = daily_data['weather'][0]['description']
        icon_data = daily_data['weather'][0]['icon']
        icon = f'http://openweathermap.org/img/w/{icon_data}.png'

    weekly_source = f'https://api.openweathermap.org/data/2.5/onecall?lat={DailyWeather.city_lat}&lon={DailyWeather.city_lon}&units=metric&exclude=current,minutely,hourly,alerts&appid={API_KEY}'
    weekly_data = requests.get(weekly_source).json()
    s = str(datetime.today().date())
    print(s)
    date = datetime.strptime(s, "%Y-%m-%d").date()
    weather_data = {}
    i = 0
    while i <= 7:
        modified_date = date + timedelta(days=i)
        datetime.strftime(modified_date, "%Y/%m/%d")
        dict1 = {i: {'day': weekly_data['daily'][i]['temp']['day'], 'night': weekly_data['daily'][i]['temp']['night'],
                     'weather': weekly_data['daily'][i]['weather'][0]['description'],
                     'humidity': weekly_data['daily'][i]['humidity'], 'date': modified_date},
                 }
        weather_data.update(dict1)
        i += 1
    print(weather_data)
    return render_template('home.html', date_time=date_time, DailyWeather=DailyWeather, WeeklyWeather=weather_data)


if __name__ == '__main__':
    app.run(debug=True)
