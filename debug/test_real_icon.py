
import time
import base64
import io
import sys
import os
import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageOps
import adafruit_ssd1306

# Allow importing from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from services import CraftyClient

def test_real_icon():
    print("--- Testing Real Icon on OLED ---")
    
    # 1. Setup OLED
    print("Initializing OLED...")
    i2c = busio.I2C(board.SCL, board.SDA)
    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
    oled.fill(0)
    oled.show()
    
    # 2. Setup Client & Fetch
    print(f"Connecting to {config.CRAFTY_URL} (Public Mode)")
    client = CraftyClient(config.CRAFTY_URL, "dummy", "dummy") # Public doesn't need real creds
    
    try:
        servers = client.get_public_server_stats()
    except Exception as e:
        print(f"Error fetching servers: {e}")
        return

    print(f"Found {len(servers)} servers.")
    
    icon_found = False
    
    for server in servers:
        name = server.get("world_name", "Unknown")
        raw_icon = server.get("icon")
        
        print(f"Checking server: {name}...")
        
        if raw_icon:
            print(f"  Icon found! Length: {len(raw_icon)}")
            # print(f"  Start of icon: {raw_icon[:50]}")
            
            try:
                # Handle Data URI
                if "," in raw_icon:
                    print("  Data URI detected, stripping prefix...")
                    raw_icon = raw_icon.split(",")[1]
                
                # Decode
                icon_data = base64.b64decode(raw_icon)
                img = Image.open(io.BytesIO(icon_data))
                
                print(f"  Image decoded. Original Size: {img.size}")
                
                # Scale up to fill height for visibility
                target_h = 48
                aspect_ratio = img.width / img.height
                target_w = int(target_h * aspect_ratio)
                
                img = img.resize((target_w, target_h), Image.HAMMING)
                img = img.convert("1")
                
                # Draw
                image = Image.new("1", (oled.width, oled.height))
                draw = ImageDraw.Draw(image)
                
                # Center
                x = (128 - target_w) // 2
                y = (64 - target_h) // 2
                
                image.paste(img, (x, y))
                draw.text((0, 0), f"Icon: {name}", fill=255)
                
                print("  Displaying icon for 10 seconds...")
                oled.image(image)
                oled.show()
                time.sleep(10)
                icon_found = True
                
            except Exception as e:
                print(f"  Error processing icon: {e}")
        else:
            print("  No icon.")
            
    if not icon_found:
        print("No server had an icon to display.")
    
    oled.fill(0)
    oled.show()
    print("Done.")

if __name__ == "__main__":
    test_real_icon()
