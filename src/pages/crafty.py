import time
import config
from PIL import Image
from .base import BaseScreen
from services import CraftyService
import utils


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
            
            # Use Utility to process icon
            processed_img = utils.process_icon_data(raw_icon, target_size=(24, 24))
            
            if processed_img:
                self.cached_icon = processed_img
                print(f"DEBUG: Icon successfully cached for {self.server_name}. Size: {self.cached_icon.size}")
            elif raw_icon and str(raw_icon) != "False":
                # If raw icon existed but processing return None, it failed.
                self.icon_processing_failed = True

        # --- Dynamic Layout Calculation ---
        has_icon = self.cached_icon is not None

        raw_desc = self.last_stats.get("desc", "")
        desc_text = ""
        if raw_desc and str(raw_desc) != "False":
            desc_text = str(raw_desc).split("\n")[0][:20]
        has_desc = len(desc_text) > 0

        # Defaults
        header_height = 15  # Compact (Title only)
        text_x = 0
        title_y = 0
        max_title_chars = 21  # Full width

        if has_icon:
            header_height = 26  # Must fit icon (24px)
            text_x = 28  # Icon (24) + Padding (4)
            max_title_chars = 15  # Reduced width

            if has_desc:
                title_y = 0
                desc_y = 12
            else:
                title_y = 6  # Vertically center title relative to icon

        elif has_desc:
            header_height = 26  # Needs 2 lines
            text_x = 0
            max_title_chars = 21
            title_y = 0
            desc_y = 12

        # --- Draw Header ---

        # Icon
        if has_icon and self.cached_icon:
            image.paste(self.cached_icon, (0, 0))

        # Title
        name_display = self.server_name[:max_title_chars]
        draw.text((text_x, title_y), name_display, font=self.font_small, fill=255)

        # Description
        if has_desc:
            # If has_icon, use same text_x. If not, use 0.
            draw.text((text_x, desc_y), desc_text, font=self.font, fill=255)

        # Separator
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
