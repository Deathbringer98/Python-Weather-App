import requests
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
import psycopg2
import csv
from psycopg2 import sql, Error

# Database connection
try:
    connection = psycopg2.connect(
        host="localhost",
        database="WeatherHistoryDB",
        user="postgres",
        password="postgres"
    )
    cursor = connection.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS WeatherRecords (
        id SERIAL PRIMARY KEY,
        city VARCHAR(100) NOT NULL,
        temperature FLOAT NOT NULL,
        pressure INT NOT NULL,
        humidity INT NOT NULL,
        wind_speed FLOAT NOT NULL,
        description VARCHAR(255) NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    connection.commit()

except Error as e:
    print(f"Database connection error: {e}")
    messagebox.showerror("Database Error", "Failed to connect to the database.")
    exit()


# Function to save weather data to the database
def save_to_db(city, temperature, pressure, humidity, wind_speed, description):
    try:
        cursor.execute("""
        INSERT INTO WeatherRecords (city, temperature, pressure, humidity, wind_speed, description)
        VALUES (%s, %s, %s, %s, %s, %s);
        """, (city, temperature, pressure, humidity, wind_speed, description))
        connection.commit()
    except Error as e:
        connection.rollback()
        print(f"Database insert error: {e}")
        messagebox.showerror("Database Error", "Failed to save data to the database.")


# Function to get weather data from API
def get_weather(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"
    try:
        response = requests.get(complete_url)
        response.raise_for_status()
        data = response.json()
        main = data['main']
        weather = data['weather'][0]
        wind = data['wind']

        temperature = main['temp']
        pressure = main['pressure']
        humidity = main['humidity']
        wind_speed = wind['speed']
        weather_description = weather['description']

        save_to_db(city_name, temperature, pressure, humidity, wind_speed, weather_description)

        weather_info = (
            f"Temperature: {temperature}°C\n"
            f"Atmospheric Pressure: {pressure} hPa\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s\n"
            f"Weather Description: {weather_description}"
        )

        return weather_info

    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        messagebox.showerror("API Error", "Failed to fetch weather data.")
        return "Error fetching data"
    except KeyError:
        return "City Not Found"


# Function to fetch weather and display
def fetch_weather():
    city_name = city_entry.get().strip()
    if city_name:
        weather_info = get_weather(city_name, api_key)
        weather_label.config(text=weather_info)
    else:
        messagebox.showwarning("Input Error", "Please enter a city name")


# Function to view historical data for a city
def view_history():
    city_name = city_entry.get().strip()
    if city_name:
        cursor.execute("SELECT * FROM WeatherRecords WHERE city = %s ORDER BY timestamp DESC", (city_name,))
        records = cursor.fetchall()

        if records:
            history_window = tk.Toplevel(root)
            history_window.title(f"Weather History for {city_name}")
            tree = ttk.Treeview(history_window, columns=(
            'ID', 'City', 'Temp', 'Pressure', 'Humidity', 'Wind Speed', 'Desc', 'Timestamp'), show='headings')
            tree.pack(fill='both', expand=True)

            for col in tree['columns']:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            for record in records:
                tree.insert('', tk.END, values=record)
        else:
            messagebox.showinfo("No Data", f"No historical data available for {city_name}.")
    else:
        messagebox.showwarning("Input Error", "Please enter a city name.")


# Function to perform basic data analysis
def analyze_data():
    cursor.execute("SELECT AVG(temperature), MAX(wind_speed) FROM WeatherRecords")
    avg_temp, max_wind = cursor.fetchone()
    messagebox.showinfo("Data Analysis",
                        f"Average Temperature: {avg_temp:.2f}°C\nHighest Wind Speed: {max_wind:.2f} m/s")


# Function to export data to CSV
def export_to_csv():
    cursor.execute("SELECT * FROM WeatherRecords")
    records = cursor.fetchall()

    if records:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ['ID', 'City', 'Temperature', 'Pressure', 'Humidity', 'Wind Speed', 'Description', 'Timestamp'])
                writer.writerows(records)
            messagebox.showinfo("Export Successful", f"Data exported to {file_path}")
    else:
        messagebox.showinfo("No Data", "No data available to export.")


# Initialize the main GUI
root = tk.Tk()
root.title("Weather App")
root.geometry("500x500")
root.configure(bg="light blue")

# Set API key
api_key = "fcdce3c23e792084b0dd11a1bd4da269"

# Input for city name
city_label = tk.Label(root, text="Enter City Name:", bg="light blue", font=("Arial", 12))
city_label.pack(pady=10)

city_entry = tk.Entry(root, font=("Arial", 12))
city_entry.pack(pady=5)

fetch_button = tk.Button(root, text="Get Weather", bg="green", font=("Arial", 12), command=fetch_weather)
fetch_button.pack(pady=10)

weather_label = tk.Label(root, text="", bg="light blue", font=("Arial", 12), justify="left")
weather_label.pack(pady=10)

# Buttons for additional features
history_button = tk.Button(root, text="View History", bg="blue", font=("Arial", 12), command=view_history)
history_button.pack(pady=5)

analyze_button = tk.Button(root, text="Analyze Data", bg="purple", font=("Arial", 12), command=analyze_data)
analyze_button.pack(pady=5)

export_button = tk.Button(root, text="Export to CSV", bg="orange", font=("Arial", 12), command=export_to_csv)
export_button.pack(pady=5)

# Canvas for cloud animation
canvas = tk.Canvas(root, bg="light blue", width=500, height=200, highlightthickness=0)
canvas.pack()

cloud_images = [
    ImageTk.PhotoImage(Image.open("cloud1.png").resize((100, 60))),
    ImageTk.PhotoImage(Image.open("cloud2.png").resize((120, 70))),
]


def animate_clouds(canvas, cloud_images, x_positions, canvas_width):
    for i, x_pos in enumerate(x_positions):
        new_x_pos = (x_pos - 2)
        if new_x_pos < -cloud_images[i].width():
            new_x_pos = canvas_width
        x_positions[i] = new_x_pos
        canvas.coords(f"cloud_{i}", new_x_pos, 50 + i * 50)

    canvas.after(50, animate_clouds, canvas, cloud_images, x_positions, canvas_width)


def setup_animation(canvas, cloud_images):
    canvas.update()
    canvas_width = canvas.winfo_width()
    x_positions = [canvas_width + i * 200 for i in range(len(cloud_images))]

    for i, img in enumerate(cloud_images):
        canvas.create_image(x_positions[i], 50 + i * 50, image=img, anchor='nw', tags=f"cloud_{i}")

    canvas.after(100, animate_clouds, canvas, cloud_images, x_positions, canvas_width)


setup_animation(canvas, cloud_images)

root.mainloop()

# Close database connection
cursor.close()
connection.close()
