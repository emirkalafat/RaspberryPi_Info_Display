from datetime import datetime
from .base import BaseScreen

class DateTimeScreen(BaseScreen):
    def draw(self, image, draw, duration):
        now = datetime.now()
        
        # Format: HH:MM:SS
        time_str = now.strftime("%H:%M:%S")
        
        # Format: DD Month YYYY
        date_str = now.strftime("%d %B %Y")
        
        # Format: Day Name
        day_str = now.strftime("%A")

        # Layout
        # Big Time
        time_bbox = self.font.getbbox(time_str) # Using main font for now, maybe need bigger if available?
        # Actually standard font is small (10px). Let's stick to what we have or scale if simple.
        # But this screen is "Detailed", so let's just center everything beautifully.
        
        # Draw Time Centered
        # To make "Big" time with small font, we can just center it.
        # Ideally we'd load a bigger font, but let's use what we have.
        
        draw.text((10, 5), time_str, font=self.font, fill=255)
        
        # Draw Date
        draw.text((10, 25), date_str, font=self.font_small, fill=255)
        
        # Draw Day
        draw.text((10, 40), day_str, font=self.font_small, fill=255)
