import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import itertools
import time


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


def fetch_weather():
    city_name = city_entry.get()
    if city_name:
        weather_info = get_weather(city_name, api_key)
        weather_label.config(text=weather_info)
    else:
        messagebox.showwarning("Input Error", "Please enter a city name")


def animate_clouds(canvas, cloud_images, x_positions, canvas_width):
    for i, x_pos in enumerate(x_positions):
        new_x_pos = (x_pos - 2)  # Adjust speed by changing this value
        if new_x_pos < -cloud_images[i].width():  # If cloud moves out of screen on the left
            new_x_pos = canvas_width  # Reset to just beyond the right side of the canvas
        x_positions[i] = new_x_pos
        canvas.coords(f"cloud_{i}", new_x_pos, 50 + i * 50)

    canvas.after(50, animate_clouds, canvas, cloud_images, x_positions, canvas_width)


def setup_animation(canvas, cloud_images):
    canvas.update()  # Ensure canvas dimensions are updated
    canvas_width = canvas.winfo_width()

    # Initialize cloud positions slightly off the screen to the right
    x_positions = [canvas_width + i * 200 for i in range(len(cloud_images))]

    # Create clouds on the canvas
    for i, img in enumerate(cloud_images):
        canvas.create_image(x_positions[i], 50 + i * 50, image=img, anchor='nw', tags=f"cloud_{i}")

    # Start animation
    canvas.after(100, animate_clouds, canvas, cloud_images, x_positions, canvas_width)


# Initialize the main GUI
root = tk.Tk()
root.title("Weather App")
root.geometry("500x400")
root.configure(bg="light blue")

# Set API key
api_key = "fcdce3c23e792084b0dd11a1bd4da269"

# Input for city name
city_label = tk.Label(root, text="Enter City Name:", bg="light blue", fg="black", font=("Arial", 12))
city_label.pack(pady=10)

city_entry = tk.Entry(root, font=("Arial", 12))
city_entry.pack(pady=5)

fetch_button = tk.Button(root, text="Get Weather", bg="green", fg="black", font=("Arial", 12), command=fetch_weather)
fetch_button.pack(pady=10)

# Weather information display
weather_label = tk.Label(root, text="", bg="light blue", fg="black", font=("Arial", 12), justify="left")
weather_label.pack(pady=10)

# Canvas for cloud animation
canvas = tk.Canvas(root, bg="light blue", width=500, height=200, highlightthickness=0)
canvas.pack()

# Load cloud images
cloud_images = [
    ImageTk.PhotoImage(Image.open("cloud1.png").resize((100, 60))),
    ImageTk.PhotoImage(Image.open("cloud2.png").resize((120, 70))),
]

setup_animation(canvas, cloud_images)

root.mainloop()
