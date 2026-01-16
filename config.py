# Crafty Controller Configuration
import os
from dotenv import load_dotenv

load_dotenv()

CRAFTY_URL = os.getenv("CRAFTY_URL", "https://localhost:8443")
CRAFTY_USERNAME = os.getenv("CRAFTY_USERNAME", "admin")
CRAFTY_PASSWORD = os.getenv("CRAFTY_PASSWORD", "default_password")

# Display Settings
DEFAULT_DURATION = 5  # Seconds per screen
SCROLL_WAIT = 2  # Seconds to wait before scrolling text (if we add that later)
