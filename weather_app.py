import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

API_KEY ="7b1ef4dd964ff9dadaddc2de8923b5c6"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city_name):
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]

        print("\n" + "=" * 40)
        print(f"  {city_name.upper()} - Weather Report")
        print("=" * 40)
        print(f"  Temperature      : {temperature}°C")
        print(f"  Feels Like       : {feels_like}°C")
        print(f"  Weather          : {description.title()}")
        print(f"  Humidity         : {humidity}%")
        print(f"  Wind Speed       : {wind_speed} m/s")
        print("=" * 40 + "\n")

    except requests.exceptions.HTTPError:
        print(f"\nError: City '{city_name}' not found. Please enter a valid city name.\n")

    except requests.exceptions.ConnectionError:
        print("\nError: No internet connection. Please check your connection.\n")

    except Exception as e:
        print(f"\nSomething went wrong: {e}\n")


def main():
    print("=== Weather App ===")
    print("Enter a city name (type 'exit' to quit)\n")

    while True:
        city = input("City name: ").strip()

        if city.lower() == "exit":
            print("Program ended. Thank you!")
            break

        if city == "":
            print("Please enter a valid city name.\n")
            continue

        get_weather(city)


if __name__ == "__main__":
    main()
