import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm


def home(request):
    return render(request, 'main/home.html')


def settings(request):
    return render(request, 'main/settings.html')


def weather(request):
    cities = City.objects.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=3539ff69d40f0b7922af06031807ef75&units=metric'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    weather_data = []

    for city in cities:
        response = requests.get(url.format(city.name))
        if response.status_code == 404:
            continue
        city_weather = response.json()

        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
            'humidity': city_weather['main']['humidity'],
            'pressure': city_weather['main']['pressure'],
            'winspeed': city_weather['wind']['speed']
        }

        weather_data.append(weather)

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'main/weather.html', context)