
import base64
import io
from PIL import Image

def process_icon_data(raw_data, target_size=(24, 24)):
    """
    Decodes a Base64 string (including data URI) into a PIL Image.
    Resizes it to target_size and converts to 1-bit mode for OLED.
    
    Args:
        raw_data (str): The raw base64 string or data URI.
        target_size (tuple): Width and Height (default 24x24).
        
    Returns:
        Image: processed PIL Image object, or None if failed.
    """
    if not raw_data or str(raw_data) == "False":
        return None

    try:
        # Handle Data URI Scheme
        if "," in raw_data:
            raw_data = raw_data.split(",")[1]

        # Decode Base64
        icon_data = base64.b64decode(raw_data)
        img = Image.open(io.BytesIO(icon_data))
        
        # Resize
        img = img.resize(target_size, Image.HAMMING)
        
        # Convert to 1-bit
        img = img.convert("1")
        
        return img
    except Exception as e:
        print(f"Icon Processing Error: {e}")
        return None
