from django.http import HttpResponse
from django.shortcuts import render

import json

import requests


# Create your views here.

def home(request):
    return render(request, 'weather/home.html')


def weather(request):
    if request.method == 'POST':
        url = 'http://dataservice.accuweather.com/locations/v1/cities/search?apikey=i8hpO8p3R5xuNyBtWHIAE5lSmJtobcxS&q={}'
        city = request.POST['city']
        list_of_data = requests.get(url.format(city)).json()
        # print(list_of_data)
        if list_of_data:
            location_data = {
                "message": "working",
                "location_name": str(list_of_data[0]["EnglishName"]),
                "Country": str(list_of_data[0]["Country"]["EnglishName"]),
                "state": str(list_of_data[0]["AdministrativeArea"]["EnglishName"]),
                "latitude": str(list_of_data[0]["GeoPosition"]["Latitude"]),
                "longitude": str(list_of_data[0]["GeoPosition"]["Longitude"]),
                "location_key": str(list_of_data[0]["Key"])
            }

            weather_url = 'http://dataservice.accuweather.com/currentconditions/v1/' + location_data[
                "location_key"] + '?apikey=i8hpO8p3R5xuNyBtWHIAE5lSmJtobcxS&details=true'
            weather_data = requests.get(weather_url).json()

            print(weather_data)

            weather_datas = {
                "temp_f": str(weather_data[0]["Temperature"]["Imperial"]["Value"]),
                "real_temp_f": str(weather_data[0]["RealFeelTemperature"]["Imperial"]["Value"]),
                "text": str(weather_data[0]["WeatherText"]),
                "WeatherIcon": int(weather_data[0]["WeatherIcon"]),
                "RelativeHumidity": int(weather_data[0]["RelativeHumidity"]),
                "Wind": int(weather_data[0]["Wind"]["Speed"]["Metric"]["Value"]),
                "Wind_Unit": str(weather_data[0]["Wind"]["Speed"]["Metric"]["Unit"]),
                "Pressure": int(weather_data[0]["Pressure"]["Metric"]["Value"]),
                "Pressure_Unit": str(weather_data[0]["Pressure"]["Metric"]["Unit"]),
                "UVIndex": int(weather_data[0]["UVIndex"]),
                "UVIndexText": str(weather_data[0]["UVIndexText"]),
                "CloudCover": int(weather_data[0]["CloudCover"]),
            }

            url = 'http://api.weatherapi.com/v1/forecast.json?key=cc1f71266946419a8ce52142201410&q={}&days=2'
            list_of_data1 = requests.get(url.format(city)).json()
            data = {
                "len1": int(len(list_of_data1['forecast']['forecastday'][0]['hour'])),
            }
            sun = {
                "sunrise": str(list_of_data1['forecast']['forecastday'][0]['astro']['sunrise']),
                "sunset": str(list_of_data1['forecast']['forecastday'][0]['astro']['sunset']),
                "local_time": str(list_of_data1['location']['localtime']),
                "is_day": str(list_of_data1['current']['is_day']),
                "coordinates": {
                    'latitude': str(list_of_data1['location']['lat']),
                    'longitude': str(list_of_data1['location']['lon'])
                },
            }
            arr = {}
            for i in range(data["len1"]):
                arr[i] = {
                    "WeatherIcon": str(list_of_data1['forecast']['forecastday'][0]['hour'][i]['condition']['icon']),
                    "IconPhrase": str(list_of_data1['forecast']['forecastday'][0]['hour'][i]['condition']['text']),
                    "time": str(list_of_data1['forecast']['forecastday'][0]['hour'][i]['time']),
                    "RainProbability": str(list_of_data1['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']),
                    "RelativeHumidity": str(list_of_data1['forecast']['forecastday'][0]['hour'][i]['humidity']),
                    "Temperature": str(list_of_data1['forecast']['forecastday'][0]['hour'][i]['temp_f']),
                    "RealFeelTemperature": str(list_of_data1['forecast']['forecastday'][0]['hour'][i]['feelslike_f']),
                    "Wind": str(list_of_data1['forecast']['forecastday'][0]['hour'][i]['wind_kph']),
                    "CloudCover": str(list_of_data1['forecast']['forecastday'][0]['hour'][i]['cloud']),
                }
            context = {
                'data': location_data,
                'weather_datas': weather_datas,
                'weather_datas_hour': arr,
                'sun': sun
            }
            return render(request, 'weather/result.html', context)
        else:
            print("empty")
            context = {
                "message": "No matching location found."
            }

    return render(request, 'weather/result.html', context)
