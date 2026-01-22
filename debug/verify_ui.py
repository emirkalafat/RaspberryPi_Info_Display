import sys
import os
from PIL import Image, ImageDraw, ImageFont

# Allow importing from parent directory
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
import config
from pages.crafty import CraftyServerScreen


# Mock Service
class MockService:
    def __init__(self, data):
        self.data = data

    def get_server_status(self, uuid):
        return self.data.get(uuid)


def verify_ui_rendering():
    print("--- Verifying UI Rendering ---")

    # 1. Setup Mock Data
    font = ImageFont.load_default()

    # CASE A: Public Mode (Players exist but no names)
    server_data_public = {"server_id": "uuid1", "server_name": "Public Server"}
    stats_public = {
        "uuid1": {
            "is_running": True,
            "player_count": 5,
            "max_players": 20,
            "player_names": [],  # Empty list provided by Public API
            "version": "1.20.4",
            "desc": "Survival Mode",
        }
    }

    # Valid 1x1 base64 GIF or PNG
    mock_icon_b64 = (
        "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"  # 1x1 White GIF
    )

    # CASE B: Auth Mode (Players exist AND names exist)
    server_data_auth = {"server_id": "uuid2", "server_name": "Auth Server"}
    stats_auth = {
        "uuid2": {
            "is_running": True,
            "player_count": 2,
            "max_players": 20,
            "player_names": ["Player1", "Player2"],
            "version": "False",  # Test skip logic
            "desc": "False",  # Test skip logic
            "icon": mock_icon_b64,
        }
    }

    # 2. Test Drawing - Public Mode
    print("\nTest Case: Public Mode (Hidden Players)")
    service_public = MockService(stats_public)
    screen_public = CraftyServerScreen(font, font, server_data_public, service_public)

    img = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(img)

    # Monkey patch draw.text to capture output
    drawn_texts = []
    original_text = draw.text

    def capture_text(xy, text, **kwargs):
        drawn_texts.append(text)
        # original_text(xy, text, **kwargs) # We don't need real drawing

    draw.text = capture_text

    screen_public.draw(img, draw, 0)

    print("Drawn Text:", drawn_texts)

    is_players_none_present = any("Players: None" in t for t in drawn_texts)
    is_players_list_present = any("Players:" in t for t in drawn_texts)

    if not is_players_none_present and not is_players_list_present:
        print("PASS: Player list correctly hidden.")
    else:
        print("FAIL: Player list text found!")

    # 3. Test Drawing - Auth Mode
    print("\nTest Case: Auth Mode (Visible Players)")
    drawn_texts = []  # Reset
    service_auth = MockService(stats_auth)
    screen_auth = CraftyServerScreen(font, font, server_data_auth, service_auth)

    # Monkey patch image.paste to verify icon drawing
    pasted_images = []

    def capture_paste(im, box=None, mask=None):
        pasted_images.append(box)

    img.paste = capture_paste

    screen_auth.draw(img, draw, 0)
    print("Drawn Text:", drawn_texts)
    print("Pasted Images (Icons):", pasted_images)

    if any("Player1" in t for t in drawn_texts):
        print("PASS: Players correctly listed.")
    else:
        print("FAIL: Players NOT listed!")

    if len(pasted_images) > 0 and pasted_images[0] == (0, 0):
        print("PASS: Icon drawn at (0,0)")
    else:
        print("FAIL: Icon NOT drawn")

    # 4. Test Layout Variations (Auth Mode as base)
    import copy
    
    # Variation 1: Icon + No Desc
    print("\nTest Case: Icon + No Desc")
    # Deep copy needed because stats works by reference
    stats_var1 = copy.deepcopy(stats_auth)
    stats_var1["uuid2"]["desc"] = "False"
    service_var1 = MockService(stats_var1)
    screen_var1 = CraftyServerScreen(font, font, server_data_auth, service_var1)
    
    # Reset capture
    drawn_texts = []
    screen_var1.draw(img, draw, 0)
    print("Drawn Text:", drawn_texts)
    
    # Variation 2: No Icon + Desc
    print("\nTest Case: No Icon + Desc")
    stats_var2 = copy.deepcopy(stats_auth)
    stats_var2["uuid2"]["desc"] = "My Description"
    stats_var2["uuid2"]["icon"] = None # Remove icon
    service_var2 = MockService(stats_var2)
    screen_var2 = CraftyServerScreen(font, font, server_data_auth, service_var2)
    
    drawn_texts = []
    screen_var2.draw(img, draw, 0)
    print("Drawn Text:", drawn_texts)

    # Variation 3: No Icon + No Desc (Compact)
    print("\nTest Case: No Icon + No Desc")
    stats_var3 = copy.deepcopy(stats_auth)
    stats_var3["uuid2"]["desc"] = "False" 
    stats_var3["uuid2"]["icon"] = None 
    service_var3 = MockService(stats_var3)
    screen_var3 = CraftyServerScreen(font, font, server_data_auth, service_var3)
    
    drawn_texts = []
    screen_var3.draw(img, draw, 0)
    print("Drawn Text:", drawn_texts)


if __name__ == "__main__":
    verify_ui_rendering()
