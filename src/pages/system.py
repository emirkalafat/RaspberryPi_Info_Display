from .base import BaseScreen
from services import SystemMonitorService

class SystemStatsScreen(BaseScreen):
    def __init__(self, font_main, font_small, monitor_service: SystemMonitorService):
        super().__init__(font_main, font_small)
        self.monitor_service = monitor_service

    def draw(self, image, draw, duration):
        # Fetch data from service
        stats = self.monitor_service.get_stats()

        # 1. Header: IP Address
        ip = stats.get("ip", "No IP")
        bbox = self.font_small.getbbox(ip)
        text_width = bbox[2] - bbox[0]
        x_pos = (image.width - text_width) // 2
        draw.text((x_pos, 0), ip, font=self.font_small, fill=255)

        # Separator
        draw.line((0, 13, image.width, 13), fill=255)

        # 2. Stats
        # CPU
        cpu = stats.get("cpu", 0)
        draw.text((0, 16), "CPU", font=self.font, fill=255)
        self.draw_bar(draw, 30, 18, 55, 8, cpu)
        draw.text((90, 16), f"{int(cpu)}%", font=self.font, fill=255)

        # RAM
        ram = stats.get("ram", 0)
        draw.text((0, 30), "RAM", font=self.font, fill=255)
        self.draw_bar(draw, 30, 32, 55, 8, ram)
        draw.text((90, 30), f"{int(ram)}%", font=self.font, fill=255)

        # Temp
        temp = stats.get("temp", 0.0)
        draw.text((0, 46), f"Temp: {temp:.1f} C", font=self.font_small, fill=255)
