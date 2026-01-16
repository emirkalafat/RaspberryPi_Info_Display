import time
import argparse
import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import config
import config
from ui import WindowManager
from services import (
    SystemMonitorService,
    CraftyService,
    WeatherService,
    FinanceService,
    CraftyClient,
)

# Import Pages
from pages.system import SystemStatsScreen
from pages.crafty import CraftyServerScreen
from pages.datetime import DateTimeScreen
from pages.weather import WeatherScreen
from pages.finance import FinanceScreen


# --- I2C Chunked Fix ---
class SSD1306_Chunked(adafruit_ssd1306.SSD1306_I2C):
    def write_framebuf(self):
        CHUNK_SIZE = 32
        for i in range(0, len(self.buffer), CHUNK_SIZE):
            chunk = self.buffer[i : i + CHUNK_SIZE]
            with self.i2c_device as i2c:
                i2c.write(b"\x40" + chunk)


# -----------------------


def main():
    parser = argparse.ArgumentParser(
        description="OLED Smart Display for Raspberry Pi & Crafty Controller"
    )
    parser.add_argument(
        "--autoscroll",
        type=bool,
        default=config.AUTO_SCROLL,
        help="Enable auto-scrolling (True/False)",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=config.DEFAULT_DURATION,
        help="Seconds to show each screen",
    )
    parser.add_argument(
        "--button-pin",
        type=int,
        default=config.BUTTON_PIN,
        help="GPIO pin for manual switching (e.g. 4)",
    )
    parser.add_argument(
        "--stats-only",
        action="store_true",
        help="Run in Stats Only mode (Disables Crafty)",
    )
    args = parser.parse_args()

    print("Initializing Smart Display...")
    print(f"Settings: Autoscroll={args.autoscroll}, Duration={args.duration}s")

    # 1. Setup I2C
    i2c = busio.I2C(board.SCL, board.SDA, frequency=100_000)
    oled = SSD1306_Chunked(
        config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT, i2c, addr=config.I2C_ADDRESS
    )
    oled.fill(0)
    oled.show()

    # 2. Setup Fonts
    try:
        font_path = config.FONT_PATH
        font = ImageFont.truetype(font_path, config.FONT_SIZE_MAIN)
        font_small = ImageFont.truetype(font_path, config.FONT_SIZE_HEADER)  # Header
    except IOError:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # 3. Initialize Services
    monitor_service = SystemMonitorService()
    weather_service = WeatherService(config.WEATHER_CONFIG)
    finance_service = FinanceService(config.FINANCE_CONFIG)
    
    # Crafty Service Init
    crafty_service = None
    authenticated = False
    
    # Determine enabled pages
    enabled_pages = config.ENABLED_PAGES[:] # Copy
    
    # Handle Stats Only Flag (Remove crafty if present)
    if args.stats_only and "crafty" in enabled_pages:
        enabled_pages.remove("crafty")
        print("Stats Only mode: Crafty disabled.")

    # Only Initialize Crafty if needed
    if "crafty" in enabled_pages:
        try:
            client = CraftyClient(
                config.CRAFTY_URL, config.CRAFTY_USERNAME, config.CRAFTY_PASSWORD
            )
            authenticated = client.login()
            if authenticated:
                crafty_service = CraftyService(client)
                print("Crafty Login Successful")
            else:
                print("Crafty Login Failed - Skipping Crafty screens")
        except Exception as e:
            print(f"Crafty Connection Error: {e}")

    # 4. Setup Window Manager & Add Screens
    wm = WindowManager(duration=args.duration, auto_scroll=args.autoscroll)

    print(f"Loading pages: {enabled_pages}")

    for page_name in enabled_pages:
        if page_name == "system":
            wm.add_screen(SystemStatsScreen(font, font_small, monitor_service))
        
        elif page_name == "datetime":
            wm.add_screen(DateTimeScreen(font, font_small))
            
        elif page_name == "weather":
            wm.add_screen(WeatherScreen(font, font_small, weather_service))
            
        elif page_name == "finance":
            wm.add_screen(FinanceScreen(font, font_small, finance_service))
            
        elif page_name == "crafty":
            if authenticated and crafty_service:
                servers = client.get_servers()
                if servers:
                    print(f"Found {len(servers)} Crafty servers.")
                    for server in servers:
                        wm.add_screen(
                            CraftyServerScreen(font, font_small, server, crafty_service)
                        )
                else:
                    print("No Crafty servers found.")

    # 5. Setup Input Button (if configured)
    button = None
    if args.button_pin:
        button = digitalio.DigitalInOut(getattr(board, f"D{args.button_pin}"))
        button.direction = digitalio.Direction.INPUT
        button.pull = digitalio.Pull.UP
        print(f"Button enabled on GPIO {args.button_pin}")

    # 6. Main Loop
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    try:
        last_button_val = True
        last_draw_time = 0

        while True:
            should_draw = False
            current_time = time.time()

            # Handle Button
            if button:
                val = button.value
                if not val and last_button_val:
                    wm.next_screen()
                    wm.auto_scroll = False
                    should_draw = True
                last_button_val = val

            # Check for regular update interval
            if current_time - last_draw_time >= config.REFRESH_INTERVAL:
                should_draw = True

            if should_draw:
                draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
                
                wm.update()
                wm.draw(image, draw)

                oled.image(image)
                oled.show()
                
                last_draw_time = current_time

            time.sleep(0.1)

    except KeyboardInterrupt:
        oled.fill(0)
        oled.show()
        print("Display Stopped.")


if __name__ == "__main__":
    main()
