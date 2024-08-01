# weather_app.py

import requests


def get_weather(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"
    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather = data['weather'][0]

        temperature = main['temp']
        pressure = main['pressure']
        humidity = main['humidity']
        weather_description = weather['description']

        weather_info = (
            f"Temperature: {temperature}°C\n"
            f"Atmospheric Pressure: {pressure} hPa\n"
            f"Humidity: {humidity}%\n"
            f"Weather Description: {weather_description}"
        )

        return weather_info
    else:
        return "City Not Found"


def main():
    api_key = "YOUR_API_KEY_HERE!"  # Your OpenWeatherMap API key
    city_name = input("Enter city name: ")
    weather_info = get_weather(city_name, api_key)
    print(weather_info)


if __name__ == "__main__":
    main()
