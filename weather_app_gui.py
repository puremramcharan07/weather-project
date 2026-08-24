import tkinter as tk
from tkinter import messagebox
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

BG_COLOR = "#0B1026"
CARD_COLOR = "#171E3A"
CARD2_COLOR = "#20294A"

WHITE = "#FFFFFF"
LIGHT_TEXT = "#C9D2E3"

BLUE = "#00C6FF"
PURPLE = "#8A5CFF"
GREEN = "#22D3A6"
ORANGE = "#FFB347"
PINK = "#FF5C8A"

def fetch_weather(city_name):

    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    response.raise_for_status()

    data = response.json()

    return {
        "city": city_name.title(),
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"].title(),
        "main": data["weather"][0]["main"],
        "wind_speed": data["wind"]["speed"]
    }

def get_weather_emoji(condition):

    icons = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️",
        "Fog": "🌫️",
        "Haze": "🌫️"
    }

    return icons.get(condition, "🌡️")

def get_weather_color(condition):

    colors = {
        "Clear": "#FFB347",
        "Clouds": "#8FA3BF",
        "Rain": "#00C6FF",
        "Drizzle": "#00C6FF",
        "Thunderstorm": "#A78BFA",
        "Snow": "#BDEBFF",
        "Mist": "#94A3B8",
        "Fog": "#94A3B8",
        "Haze": "#FBBF24"
    }

    return colors.get(condition, BLUE)

def get_weather():

    city = city_entry.get().strip()

    if city == "":
        messagebox.showwarning(
            "Input Required",
            "Please enter a city name."
        )
        return

    try:

        weather = fetch_weather(city)

        emoji = get_weather_emoji(weather["main"])
        weather_color = get_weather_color(weather["main"])

        # City
        city_label.config(
            text=f"{emoji}  {weather['city']}"
        )

        # Temperature
        temp_label.config(
            text=f"{weather['temperature']:.1f}°C",
            fg=weather_color
        )

        # Description
        desc_label.config(
            text=weather["description"]
        )

        # Feels Like
        feels_value.config(
            text=f"{weather['feels_like']:.1f}°C"
        )

        # Humidity
        humidity_value.config(
            text=f"{weather['humidity']}%"
        )

        # Wind
        wind_value.config(
            text=f"{weather['wind_speed']} m/s"
        )

        # Show result
        result_frame.pack(
            pady=20,
            padx=30,
            fill="x"
        )

        # Status
        status_label.config(
            text="● Weather updated successfully",
            fg=GREEN
        )

    except requests.exceptions.HTTPError:

        messagebox.showerror(
            "City Not Found",
            f"City '{city}' not found.\nPlease check the spelling."
        )

        result_frame.pack_forget()

    except requests.exceptions.ConnectionError:

        messagebox.showerror(
            "Connection Error",
            "No internet connection.\nPlease check your connection."
        )

        result_frame.pack_forget()

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Something went wrong:\n{e}"
        )

        result_frame.pack_forget()

root = tk.Tk()

root.title("Weather App")

root.geometry("520x700")

root.resizable(False, False)

root.configure(bg=BG_COLOR)

header = tk.Frame(
    root,
    bg=BG_COLOR
)

header.pack(
    pady=(30, 10)
)


title_label = tk.Label(
    header,
    text="🌤️ Weather App",
    font=("Segoe UI", 28, "bold"),
    bg=BG_COLOR,
    fg=WHITE
)

title_label.pack()


subtitle_label = tk.Label(
    header,
    text="Check real-time weather anywhere 🌍",
    font=("Segoe UI", 11),
    bg=BG_COLOR,
    fg=LIGHT_TEXT
)

subtitle_label.pack(
    pady=(5, 0)
)

search_container = tk.Frame(
    root,
    bg=CARD_COLOR
)

search_container.pack(
    padx=30,
    pady=20,
    fill="x"
)


city_entry = tk.Entry(
    search_container,
    font=("Segoe UI", 14),
    bg="#FFFFFF",
    fg="#111827",
    insertbackground="#111827",
    bd=0,
    relief="flat"
)

city_entry.pack(
    side="left",
    padx=15,
    pady=15,
    ipady=9,
    fill="x",
    expand=True
)


search_button = tk.Button(
    search_container,
    text="🔍 Search",
    font=("Segoe UI", 11, "bold"),
    bg=PURPLE,
    fg=WHITE,
    activebackground="#7048D8",
    activeforeground=WHITE,
    bd=0,
    relief="flat",
    cursor="hand2",
    command=get_weather
)

search_button.pack(
    side="right",
    padx=(0, 15),
    pady=15,
    ipadx=12,
    ipady=9
)

status_label = tk.Label(
    root,
    text="● Enter a city to get weather",
    font=("Segoe UI", 10),
    bg=BG_COLOR,
    fg=LIGHT_TEXT
)

status_label.pack(
    pady=(0, 5)
)

result_frame = tk.Frame(
    root,
    bg=CARD_COLOR
)

city_label = tk.Label(
    result_frame,
    text="",
    font=("Segoe UI", 22, "bold"),
    bg=CARD_COLOR,
    fg=WHITE
)

city_label.pack(
    pady=(25, 5)
)

temp_label = tk.Label(
    result_frame,
    text="",
    font=("Segoe UI", 52, "bold"),
    bg=CARD_COLOR,
    fg=BLUE
)

temp_label.pack()

desc_label = tk.Label(
    result_frame,
    text="",
    font=("Segoe UI", 14),
    bg=CARD_COLOR,
    fg=LIGHT_TEXT
)

desc_label.pack(
    pady=(0, 25)
)

details_frame = tk.Frame(
    result_frame,
    bg=CARD_COLOR
)

details_frame.pack(
    padx=20,
    pady=(0, 25),
    fill="x"
)


# Feels Like

feels_card = tk.Frame(
    details_frame,
    bg=CARD2_COLOR
)

feels_card.pack(
    side="left",
    padx=5,
    expand=True,
    fill="both"
)


tk.Label(
    feels_card,
    text="🌡️",
    font=("Segoe UI", 20),
    bg=CARD2_COLOR,
    fg=WHITE
).pack(pady=(15, 3))


tk.Label(
    feels_card,
    text="Feels Like",
    font=("Segoe UI", 9),
    bg=CARD2_COLOR,
    fg=LIGHT_TEXT
).pack()


feels_value = tk.Label(
    feels_card,
    text="-",
    font=("Segoe UI", 14, "bold"),
    bg=CARD2_COLOR,
    fg=WHITE
)

feels_value.pack(
    pady=(3, 15)
)


# Humidity

humidity_card = tk.Frame(
    details_frame,
    bg=CARD2_COLOR
)

humidity_card.pack(
    side="left",
    padx=5,
    expand=True,
    fill="both"
)


tk.Label(
    humidity_card,
    text="💧",
    font=("Segoe UI", 20),
    bg=CARD2_COLOR,
    fg=WHITE
).pack(pady=(15, 3))


tk.Label(
    humidity_card,
    text="Humidity",
    font=("Segoe UI", 9),
    bg=CARD2_COLOR,
    fg=LIGHT_TEXT
).pack()


humidity_value = tk.Label(
    humidity_card,
    text="-",
    font=("Segoe UI", 14, "bold"),
    bg=CARD2_COLOR,
    fg=GREEN
)

humidity_value.pack(
    pady=(3, 15)
)


# Wind

wind_card = tk.Frame(
    details_frame,
    bg=CARD2_COLOR
)

wind_card.pack(
    side="left",
    padx=5,
    expand=True,
    fill="both"
)


tk.Label(
    wind_card,
    text="💨",
    font=("Segoe UI", 20),
    bg=CARD2_COLOR,
    fg=WHITE
).pack(pady=(15, 3))


tk.Label(
    wind_card,
    text="Wind Speed",
    font=("Segoe UI", 9),
    bg=CARD2_COLOR,
    fg=LIGHT_TEXT
).pack()


wind_value = tk.Label(
    wind_card,
    text="-",
    font=("Segoe UI", 14, "bold"),
    bg=CARD2_COLOR,
    fg=ORANGE
)

wind_value.pack(
    pady=(3, 15)
)

footer = tk.Label(
    root,
    text="🌍 Powered by OpenWeather API",
    font=("Segoe UI", 9),
    bg=BG_COLOR,
    fg="#718096"
)

footer.pack(
    side="bottom",
    pady=15
)

root.bind(
    "<Return>",
    lambda event: get_weather()
)


root.mainloop()