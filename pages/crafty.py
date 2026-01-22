import time
import base64
import io
import config
from PIL import Image, ImageOps
from .base import BaseScreen
from services import CraftyService


class CraftyServerScreen(BaseScreen):
    def __init__(
        self, font_main, font_small, server_data, crafty_service: CraftyService
    ):
        super().__init__(font_main, font_small)
        # Fix: Use 'server_id' instead of 'server_uuid'
        self.server_uuid = server_data.get("server_id")
        self.server_name = server_data.get("server_name", "Unknown")
        self.crafty_service = crafty_service
        self.last_stats = None
        self.cached_icon = None
        self.icon_processing_failed = False

    def draw(self, image, draw, duration):
        # Stats are now fetched in background by service
        # Just retrieve immediately
        self.last_stats = self.crafty_service.get_server_status(self.server_uuid)

        if self.last_stats and not self.cached_icon and not self.icon_processing_failed:
            raw_icon = self.last_stats.get("icon")
            if raw_icon and str(raw_icon) != "False":
                try:
                    # Handle Data URI Scheme (e.g. data:image/png;base64,....)
                    if "," in raw_icon:
                        raw_icon = raw_icon.split(",")[1]

                    # Decode Base64
                    icon_data = base64.b64decode(raw_icon)
                    img = Image.open(io.BytesIO(icon_data))

                    # Resize to 24x24 for Header Area
                    img = img.resize((24, 24), Image.HAMMING)

                    # Convert to 1-bit
                    img = img.convert("1")
                    self.cached_icon = img
                except Exception as e:
                    print(f"Icon Decode Error: {e}")
                    self.icon_processing_failed = True
            if self.cached_icon:
                print(
                    f"DEBUG: Icon successfully cached for {self.server_name}. Size: {self.cached_icon.size}"
                )

        # Layout Constants
        header_height = 26
        icon_size = 24
        text_x = 0

        # Draw Icon
        if self.cached_icon:
            image.paste(self.cached_icon, (0, 0))
            text_x = icon_size + 4  # Padding

        # Line 1: Server Name (Header)
        name_display = self.server_name[:15]  # Shorten slighty to fit
        draw.text((text_x, 0), name_display, font=self.font_small, fill=255)

        # Line 2: Description (Small, no prefix)
        desc = self.last_stats.get("desc", "")
        if desc and str(desc) != "False":
            # Only show first line, truncated
            desc_display = str(desc).split("\n")[0][:20]
            draw.text((text_x, 12), desc_display, font=self.font, fill=255)

        # Separator (Below icon/header)
        draw.line((0, header_height, image.width, header_height), fill=255)

        if self.last_stats:
            is_running = self.last_stats.get("is_running", False)

            if is_running:
                # Content starts below separator
                current_y = header_height + 2

                player_count = self.last_stats.get("player_count", 0)
                max_players = self.last_stats.get("max_players", "0")
                player_names = self.last_stats.get("player_names", [])

                # Line 3: Online X/Y
                draw.text(
                    (0, current_y),
                    f"Online {player_count}/{max_players}",
                    font=self.font,
                    fill=255,
                )
                current_y += 12

                # Line 4: Version (if present)
                version = self.last_stats.get("version", "")
                if version and str(version) != "False":
                    draw.text(
                        (0, current_y),
                        f"Ver: {str(version)[:15]}",
                        font=self.font,
                        fill=255,
                    )
                    current_y += 12

                # Separator if details were shown, to space out players
                if current_y > 28:
                    current_y += 2

                # Line 4+: Players: name1 name2...
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
                    y = current_y
                    for line in lines:
                        if y > image.height - 10:
                            break  # Clip check
                        draw.text((0, y), line.strip(), font=self.font, fill=255)
                        y += 12
                # else:
                #    Do not show "Players: None" because it might be misleading in Public Mode
                #    (where Count > 0 but Names are empty).

            else:
                draw.text(
                    (0, header_height + 4), "Status: Offline", font=self.font, fill=255
                )
        else:
            # Only show loading if we have NEVER retrieved stats
            draw.text((0, 25), "Loading...", font=self.font, fill=255)
