import time
from weather import get_weather_data, process_weather_data, generate_daily_summary

# List of cities to monitor
cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]

# Configurable interval (e.g., every 5 minutes)
INTERVAL = 300  # seconds

# Alert thresholds (example: alert if temperature exceeds 35°C)
TEMP_THRESHOLD = 35.0  
CONSECUTIVE_ALERTS = 2  

# Function to monitor weather and process rollups
def monitor_weather(interval=INTERVAL):
    city_alert_counts = {city: 0 for city in cities}  
    daily_weather_data = []  

    while True:
        for city in cities:
            try:
                # Fetch and process data for each city
                raw_data = get_weather_data(city)
                processed_data = process_weather_data(raw_data, city)
                daily_weather_data.append(processed_data)

                # Print the processed weather data
                print(f"Processed Weather Data for {city}: {processed_data}")

                # Check if alert conditions are met
                if processed_data["temperature"] > TEMP_THRESHOLD:
                    city_alert_counts[city] += 1
                    if city_alert_counts[city] >= CONSECUTIVE_ALERTS:
                        print(f"ALERT: Temperature in {city} has exceeded {TEMP_THRESHOLD}°C for {CONSECUTIVE_ALERTS} consecutive readings!")
                else:
                    city_alert_counts[city] = 0  

            except Exception as e:
                print(f"Error fetching weather for {city}: {e}")

        # Generate daily summary at the end of the day or periodically
        if daily_weather_data:
            daily_summary = generate_daily_summary(daily_weather_data)
            print("\nDaily Summary:", daily_summary)

            # Clear daily data after generating the summary
            daily_weather_data.clear()

        # Wait for the specified interval before the next update
        print(f"\nWaiting for {interval} seconds before the next update...\n")
        time.sleep(interval)

if __name__ == '__main__':
    print("Starting Weather Monitoring System...")
    monitor_weather()
