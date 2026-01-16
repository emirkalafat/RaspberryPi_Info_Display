import time
import argparse
import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import config
from crafty import CraftyClient
from ui import WindowManager, SystemStatsScreen, CraftyServerScreen
from services import SystemMonitorService, CraftyService  # Import Services


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
        help="Run in Stats Only mode (ignore config.STATS_ONLY)",
    )
    args = parser.parse_args()

    print("Initializing Smart Display...")
    is_stats_only = args.stats_only or config.STATS_ONLY
    print(
        f"Settings: Autoscroll={args.autoscroll}, Duration={args.duration}s, StatsOnly={is_stats_only}"
    )

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

    # 3. Setup Services
    monitor_service = SystemMonitorService()

    authenticated = False
    client = None
    crafty_service = None

    if not is_stats_only:
        client = CraftyClient(
            config.CRAFTY_URL, config.CRAFTY_USERNAME, config.CRAFTY_PASSWORD
        )
        crafty_service = CraftyService(client)
        authenticated = client.login()

    # 4. Setup Window Manager
    wm = WindowManager(duration=args.duration, auto_scroll=args.autoscroll)

    # Add Screens
    # a) System Stats (Inject Service)
    wm.add_screen(SystemStatsScreen(font, font_small, monitor_service))

    # b) Crafty Servers (if authenticated and NOT stats only)
    if authenticated and not is_stats_only:
        servers = client.get_servers()
        if servers:
            print(f"Found {len(servers)} servers.")
            for server in servers:
                # Add a screen for each server (Inject Service)
                wm.add_screen(
                    CraftyServerScreen(font, font_small, server, crafty_service)
                )
        else:
            print("No servers found or API error.")
    elif is_stats_only:
        print("Running in Stats Only mode (per config or flag).")
    else:
        print("Running in System Stats only mode (Crafty login failed).")

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
        last_button_val = True  # Pull-UP means default High
        last_draw_time = 0

        while True:
            should_draw = False
            current_time = time.time()

            # Handle Button
            if button:
                val = button.value
                if not val and last_button_val:  # Falling edge (Pressed)
                    wm.next_screen()
                    wm.auto_scroll = False  # Disable auto-scroll if user interacts?
                    should_draw = True # Force draw on interaction
                last_button_val = val

            # Check for regular update interval
            if current_time - last_draw_time >= config.REFRESH_INTERVAL:
                should_draw = True

            if should_draw:
                # Clear buffer
                draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
                
                # Update & Draw
                wm.update()
                wm.draw(image, draw)

                oled.image(image)
                oled.show()
                
                last_draw_time = current_time

            time.sleep(0.1)  # Fast loop for button responsiveness

    except KeyboardInterrupt:
        oled.fill(0)
        oled.show()
        print("Display Stopped.")


if __name__ == "__main__":
    main()
