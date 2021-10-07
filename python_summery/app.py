import requests
from flask import Flask, config, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    API_KEY = 'c1cc30025fb6b54818285feab2ece25f'
    # If there is no city name provided, get user's location and display that city weather:
    if request.method == 'POST':
        city_name = request.form['city-name']
    else:
        city_name = "jerusalem"
    daily_source = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={API_KEY}'
    daily_data = requests.get(daily_source).json()
    print(daily_data)

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

        #today = get_date(datetime_get)

    weekly_source = f'https://api.openweathermap.org/data/2.5/onecall?lat={DailyWeather.city_lat}&lon={DailyWeather.city_lon}&units=metric&exclude=current,minutely,hourly,alerts&appid={API_KEY}'
    weekly_data = requests.get(weekly_source).json()

    weather_data = {}
    i = 0
    while i <= 7:
        dict1 = {i: {'day': weekly_data['daily'][i]['temp']['day'], 'night': weekly_data['daily'][i]['temp']['night'],
                     'weather': weekly_data['daily'][i]['weather'][0]['description'],
                     'humidity': weekly_data['daily'][i]['humidity']},
                 }
        weather_data.update(dict1)
        i += 1
    print(weather_data)
    return render_template('home.html', DailyWeather=DailyWeather, WeeklyWeather=weather_data)


if __name__ == '__main__':
    app.run(debug=True)
