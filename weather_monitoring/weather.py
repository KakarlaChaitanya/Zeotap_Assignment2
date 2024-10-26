import requests
import os
from datetime import datetime

# Base URL for OpenWeatherMap API
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# Retrieve the API key from environment variables
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# List of cities to monitor
cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]

def get_weather_data(city):
    """
    Fetches weather data for a given city from OpenWeatherMap API.
    """
    if not API_KEY:
        raise Exception("OpenWeatherMap API key not found. Please set OPENWEATHER_API_KEY.")
    
    # Complete API URL for the specified city
    url = f"{BASE_URL}q={city}&appid={API_KEY}"
    
    # Make the API request
    response = requests.get(url)
    data = response.json()
    
    if response.status_code != 200:
        raise Exception(f"Failed to get data for {city}: {data.get('message', 'Unknown error')}")
    
    return data

def kelvin_to_celsius(kelvin_temp):
    """
    Converts temperature from Kelvin to Celsius.
    """
    return kelvin_temp - 273.15

def process_weather_data(data, city):
    """
    Processes and formats the weather data to include temperature, feels like temperature,
    weather condition, and timestamp.
    """
    main_data = data['main']
    weather_condition = data['weather'][0]['main']
    temperature = kelvin_to_celsius(main_data['temp'])
    feels_like = kelvin_to_celsius(main_data['feels_like'])
    timestamp = datetime.utcfromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
    
    processed_data = {
        "city": city,
        "temperature": round(temperature, 2),
        "feels_like": round(feels_like, 2),
        "condition": weather_condition,
        "timestamp": timestamp
    }
    
    return processed_data

def generate_daily_summary(weather_data_list):
    """
    Generates a daily summary with average, minimum, maximum temperatures,
    and the most common weather condition.
    """
    temperatures = [data["temperature"] for data in weather_data_list]
    conditions = [data["condition"] for data in weather_data_list]
    
    average_temp = round(sum(temperatures) / len(temperatures), 2)
    min_temp = round(min(temperatures), 2)
    max_temp = round(max(temperatures), 2)
    dominant_condition = max(set(conditions), key=conditions.count)
    
    summary = {
        "average_temp": average_temp,
        "min_temp": min_temp,
        "max_temp": max_temp,
        "dominant_condition": dominant_condition,
        "date": datetime.now().strftime('%Y-%m-%d')
    }
    
    return summary

# Example usage
if __name__ == "__main__":
    weather_data_list = []
    
    for city in cities:
        try:
            # Fetch and process data for each city
            raw_data = get_weather_data(city)
            processed_data = process_weather_data(raw_data, city)
            weather_data_list.append(processed_data)
            
            # Print the processed data
            print(f"Processed Weather Data for {city}: {processed_data}")
        
        except Exception as e:
            print(f"Error fetching weather for {city}: {e}")
    
    # Generate and display daily summary
    if weather_data_list:
        daily_summary = generate_daily_summary(weather_data_list)
        print("\nDaily Summary:", daily_summary)
