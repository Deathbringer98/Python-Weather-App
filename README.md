## Python Weather App
A simple Python script that uses the free OpenWeatherMap API to fetch and display weather information based on the user's city. This app also provides additional functionalities such as viewing historical data, performing basic data analysis, and exporting data to a CSV file.

## Features
Fetch current weather data for a specified city.
Display temperature, atmospheric pressure, humidity, wind speed, and weather description.
Store weather data in a PostgreSQL database for historical tracking.
Historical Data Viewer: View past weather records for a specified city.
Data Analysis: Calculate and display the average temperature and highest wind speed.
Export to CSV: Export all saved weather data to a CSV file.
Prerequisites
Python 3.x
Required Python libraries:
requests
tkinter
Pillow
psycopg2
You can install the required libraries using pip:

pip install requests Pillow psycopg2
Getting Started
Clone the repository:

git clone https://github.com/Deathbringer98/Python-Weather-App.git
cd Python-Weather-App
Obtain a free API key from OpenWeatherMap.

Open weather_app.py and replace "your_api_key_here" with your actual API key:

api_key = "your_api_key_here"  # Replace with your OpenWeatherMap API key
Set up your PostgreSQL database:

Ensure PostgreSQL is installed and running.
Create a database named WeatherHistoryDB.
Update your PostgreSQL username and password in weather_app.py.
Run the script:


python weather_app.py
Enter the city name in the application to fetch weather data.

Example Data
yaml
Copy code
Enter city name: Toronto
Temperature: 7.8°C
Atmospheric Pressure: 1016 hPa
Humidity: 81%
Wind Speed: 3.09 m/s
Weather Description: overcast clouds
Additional Features
Historical Data Viewer
View past weather data for a city.
Access this feature via the "View History" button in the app.
Data Analysis
Calculate the average temperature and highest wind speed across all records.
Access this feature via the "Analyze Data" button.
Export to CSV
Export all weather records to a CSV file.
Access this feature via the "Export to CSV" button.

# PICS 


![v](https://github.com/user-attachments/assets/d49648f2-26f7-4bea-8ceb-0ed271d745fe)


![Screenshot 2024-11-15 183746](https://github.com/user-attachments/assets/d1fba1c7-16c1-4c2e-947f-597daf370c6f)
