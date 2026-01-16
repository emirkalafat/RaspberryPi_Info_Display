import time
from PIL import ImageDraw, ImageFont
import config


class WindowManager:
    def __init__(self, start_screen=0, duration=5, auto_scroll=True):
        self.screens = []
        self.current_screen_index = start_screen
        self.last_switch_time = time.time()
        self.duration = duration
        self.auto_scroll = auto_scroll

    def add_screen(self, screen):
        self.screens.append(screen)

    def next_screen(self):
        self.current_screen_index = (self.current_screen_index + 1) % len(self.screens)
        self.last_switch_time = time.time()

    def update(self):
        """Checks if it's time to switch screens."""
        if self.auto_scroll and len(self.screens) > 1:
            if time.time() - self.last_switch_time > self.duration:
                self.next_screen()

    def draw(self, image, draw):
        """Draws the current screen."""
        if not self.screens:
            draw.text((10, 20), "No Screens", fill=255)
            return

        current_screen = self.screens[self.current_screen_index]
        current_screen.draw(image, draw, self.duration)


class BaseScreen:
    def __init__(self, font_main, font_small):
        self.font = font_main
        self.font_small = font_small

    def draw(self, image, draw, duration):
        pass

    def draw_bar(self, draw, x, y, width, height, percent):
        # Draw outline
        draw.rectangle((x, y, x + width, y + height), outline=255, fill=0)
        # Draw fill
        fill_width = int(width * (percent / 100.0))
        if fill_width > 0:
            draw.rectangle((x, y, x + fill_width, y + height), outline=None, fill=255)


class SystemStatsScreen(BaseScreen):
    def __init__(self, font_main, font_small, monitor_service):
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


class CraftyServerScreen(BaseScreen):
    def __init__(self, font_main, font_small, server_data, crafty_service):
        super().__init__(font_main, font_small)
        # Fix: Use 'server_id' instead of 'server_uuid'
        self.server_uuid = server_data.get("server_id")
        self.server_name = server_data.get("server_name", "Unknown")
        self.crafty_service = crafty_service
        self.last_stats = None
        self.last_update = 0
        self.update_interval = (
            config.UPDATE_INTERVAL
        )  # Slow down refresh rate to value in config

    def draw(self, image, draw, duration):
        # Update stats if needed
        # Robustness Fix: Only overwrite last_stats if new fetch is successful
        if time.time() - self.last_update > self.update_interval:
            new_stats = self.crafty_service.get_server_status(self.server_uuid)
            if new_stats:
                self.last_stats = new_stats
            self.last_update = time.time()

        # Header: Server Name
        name_display = self.server_name[:18]
        draw.text((0, 0), name_display, font=self.font_small, fill=255)

        # Separator
        draw.line((0, 13, image.width, 13), fill=255)

        if self.last_stats:
            is_running = self.last_stats.get("is_running", False)

            if is_running:
                player_count = self.last_stats.get("player_count", 0)
                max_players = self.last_stats.get("max_players", "0")
                player_names = self.last_stats.get("player_names", [])

                # Line 1: Online X/Y
                draw.text(
                    (0, 16),
                    f"Online {player_count}/{max_players}",
                    font=self.font,
                    fill=255,
                )

                # Line 2+: Players: name1 name2...
                if player_names:
                    names_str = "Players: " + " ".join(player_names)

                    # Word Wrap
                    words = names_str.split(" ")
                    lines = []
                    current_line = ""

                    for word in words:
                        test_line = current_line + word + " "
                        bbox = self.font.getbbox(test_line)
                        w = bbox[2] - bbox[0]
                        if w < image.width:
                            if len(current_line) == 0:
                                lines.append(word)
                                current_line = ""
                            else:
                                current_line = test_line
                        else:
                            lines.append(current_line)
                            current_line = word + " "
                    if current_line:
                        lines.append(current_line)

                    # Draw lines
                    y = 30
                    for line in lines:
                        if y > image.height - 10:
                            break  # Clip check
                        draw.text((0, y), line.strip(), font=self.font, fill=255)
                        y += 12
                else:
                    draw.text((0, 30), "Players: None", font=self.font, fill=255)

            else:
                draw.text((0, 16), "Status: Offline", font=self.font, fill=255)
        else:
            # Only show loading if we have NEVER retrieved stats
            draw.text((0, 25), "Loading...", font=self.font, fill=255)
