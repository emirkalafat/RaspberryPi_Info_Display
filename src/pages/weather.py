import time
from .base import BaseScreen
from services import WeatherService

class WeatherScreen(BaseScreen):
    def __init__(self, font_main, font_small, weather_service: WeatherService):
        super().__init__(font_main, font_small)
        self.weather_service = weather_service
        self.last_data = None
        self.last_update = 0
        self.update_interval = 1800  # Update every 30 minutes

    def _get_status_text(self, code):
        if code == 0: return "Clear Sky"
        if code in [1, 2, 3]: return "Partly Cloudy"
        if code in [45, 48]: return "Foggy"
        if code in [51, 53, 55]: return "Drizzle"
        if code in [56, 57]: return "Freezing Drizzle"
        if code in [61, 63, 65]: return "Rain"
        if code in [66, 67]: return "Freezing Rain"
        if code in [71, 73, 75]: return "Snow"
        if code == 77: return "Snow Grains"
        if code in [80, 81, 82]: return "Rain Showers"
        if code in [85, 86]: return "Snow Showers"
        if code >= 95: return "Thunderstorm"
        return "Unknown"

    def draw(self, image, draw, duration):
        # Update weather data
        if time.time() - self.last_update > self.update_interval or self.last_data is None:
            data = self.weather_service.get_weather()
            if data:
                self.last_data = data
                self.last_update = time.time()

        if self.last_data:
            city = self.last_data.get("city", "Unknown")
            temp = self.last_data.get("temp", 0)
            code = self.last_data.get("code", 0)
            status = self._get_status_text(code)

            # Draw
            # Header: City
            draw.text((0, 0), city, font=self.font_small, fill=255)
            draw.line((0, 13, image.width, 13), fill=255)

            # Temp (Centered-ish)
            temp_str = f"{temp:.1f}C"
            # Using main font, maybe scale it up if possible? 
            # For now standard font.
            draw.text((10, 20), temp_str, font=self.font, fill=255)

            # Status
            draw.text((10, 35), status, font=self.font_small, fill=255)
            
            # Last Update Time (Small)
            update_time = time.strftime("%H:%M", time.localtime(self.last_update))
            draw.text((80, 50), update_time, font=self.font_small, fill=255)

        else:
            draw.text((10, 25), "Loading Weather...", font=self.font, fill=255)
