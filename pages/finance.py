import time
from .base import BaseScreen
from services import FinanceService

class FinanceScreen(BaseScreen):
    def __init__(self, font_main, font_small, finance_service: FinanceService):
        super().__init__(font_main, font_small)
        self.finance_service = finance_service
        self.last_data = {}
        self.last_update = 0
        self.update_interval = 3600  # Update every hour (since it's daily data mostly, or liveish)

    def draw(self, image, draw, duration):
        # Update
        if time.time() - self.last_update > self.update_interval or not self.last_data:
            data = self.finance_service.get_data()
            if data:
                self.last_data = data
                self.last_update = time.time()
        
        # Header
        draw.text((30, 0), "Market (TRY)", font=self.font_small, fill=255)
        draw.line((0, 13, image.width, 13), fill=255)
        
        if self.last_data:
            y = 16
            # USD
            usd = self.last_data.get("USD", 0)
            if usd:
                draw.text((5, y), f"USD: {usd:.2f}", font=self.font, fill=255)
                y += 12
            
            # EUR
            eur = self.last_data.get("EUR", 0)
            if eur:
                draw.text((5, y), f"EUR: {eur:.2f}", font=self.font, fill=255)
                y += 12
                
            # Gold
            gold = self.last_data.get("GOLD", 0)
            if gold:
                draw.text((5, y), f"Gram: {gold:.0f}", font=self.font, fill=255)
                
        else:
            draw.text((10, 25), "Loading..", font=self.font, fill=255)
