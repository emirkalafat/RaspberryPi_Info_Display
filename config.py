import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Function to load config
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if not os.path.exists(config_path):
        print(f"Warning: {config_path} not found. Using defaults.")
        return {}

    with open(config_path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding config.json: {e}")
            return {}


_config_data = load_config()


# Helper to get nested keys safely
def get_setting(path, default=None):
    keys = path.split(".")
    value = _config_data
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    return value


# --- Exported Settings ---

# Crafty Controller
CRAFTY_URL = get_setting("crafty.url", "https://localhost:8443")
CRAFTY_USERNAME = os.getenv("CRAFTY_USERNAME", "admin")
CRAFTY_PASSWORD = os.getenv("CRAFTY_PASSWORD", "default_password")

# Display
DISPLAY_WIDTH = get_setting("display.width", 128)
DISPLAY_HEIGHT = get_setting("display.height", 64)
I2C_ADDRESS = int(get_setting("display.i2c_address", "0x3C"), 16)
DEFAULT_DURATION = get_setting("display.default_duration", 5)
AUTO_SCROLL = get_setting("display.auto_scroll", True)
STATS_ONLY = get_setting("display.stats_only", False)

# Fonts
FONT_PATH = get_setting("fonts.path", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
FONT_SIZE_MAIN = get_setting("fonts.size_main", 10)
FONT_SIZE_HEADER = get_setting("fonts.size_header", 11)

# GPIO
BUTTON_PIN = get_setting("gpio.button_pin", None)

# System
UPDATE_INTERVAL = get_setting("system.update_interval", 10)
