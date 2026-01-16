from .base import BackgroundService

class WeatherService(BackgroundService):
    def __init__(self, config):
        self.lat = config.get("lat")
        self.lon = config.get("lon")
        self.city = config.get("city", "Unknown")
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        super().__init__(update_interval=1800) # 30 mins

    def fetch_data(self):
        # Renamed from get_weather to fetch_data
        try:
            params = {
                "latitude": self.lat,
                "longitude": self.lon,
                "current": "temperature_2m,weather_code",
                "timezone": "auto"
            }
            # Import locally to avoid top-level dependency issues if not installed
            import requests
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current", {})
            return {
                "temp": current.get("temperature_2m", 0),
                "code": current.get("weather_code", 0),
                "city": self.city
            }
        except Exception as e:
            print(f"Weather API Error: {e}")
            return None
            
    # Alias for compatibility if needed, or update call sites
    def get_weather(self):
        return self.get_data()
