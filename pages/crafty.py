import time
import config
from .base import BaseScreen
from services import CraftyService

class CraftyServerScreen(BaseScreen):
    def __init__(self, font_main, font_small, server_data, crafty_service: CraftyService):
        super().__init__(font_main, font_small)
        # Fix: Use 'server_id' instead of 'server_uuid'
        self.server_uuid = server_data.get("server_id")
        self.server_name = server_data.get("server_name", "Unknown")
        self.crafty_service = crafty_service
        self.last_stats = None
    def draw(self, image, draw, duration):
        # Stats are now fetched in background by service
        # Just retrieve immediately
        self.last_stats = self.crafty_service.get_server_status(self.server_uuid)

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
