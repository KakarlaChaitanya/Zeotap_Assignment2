import pytest
import os
from weather import get_weather_data, process_weather_data, generate_daily_summary

# Mock the environment variable for API key
os.environ["OPENWEATHER_API_KEY"] = "test_api_key"

# Mock data for testing
mock_api_response = {
    "main": {
        "temp": 300.15,  # Kelvin
        "feels_like": 298.15,  # Kelvin
    },
    "weather": [{"main": "Clear"}],
    "dt": 1633024800  # Sample timestamp
}

mock_processed_data = {
    "city": "TestCity",
    "temperature": 27.0,  # Celsius
    "feels_like": 25.0,  # Celsius
    "condition": "Clear",
    "timestamp": "2021-10-01 00:00:00"
}

mock_weather_data_list = [
    {"temperature": 27.0, "condition": "Clear"},
    {"temperature": 29.0, "condition": "Rain"},
    {"temperature": 25.0, "condition": "Clear"},
    {"temperature": 30.0, "condition": "Clouds"},
    {"temperature": 28.0, "condition": "Clear"}
]

# Test get_weather_data
def test_get_weather_data(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return mock_api_response
        return MockResponse()
    
    monkeypatch.setattr("requests.get", mock_get)
    
    data = get_weather_data("TestCity")
    assert data["main"]["temp"] == mock_api_response["main"]["temp"]
    assert data["weather"][0]["main"] == mock_api_response["weather"][0]["main"]

# Test process_weather_data
def test_process_weather_data():
    processed_data = process_weather_data(mock_api_response, "TestCity")
    assert processed_data["city"] == mock_processed_data["city"]
    assert round(processed_data["temperature"], 1) == mock_processed_data["temperature"]
    assert round(processed_data["feels_like"], 1) == mock_processed_data["feels_like"]
    assert processed_data["condition"] == mock_processed_data["condition"]
    assert processed_data["timestamp"] == mock_processed_data["timestamp"]

# Test generate_daily_summary
def test_generate_daily_summary():
    summary = generate_daily_summary(mock_weather_data_list)
    
    assert summary["average_temp"] == 27.8  
    assert summary["min_temp"] == 25.0
    assert summary["max_temp"] == 30.0
    assert summary["dominant_condition"] == "Clear" 
