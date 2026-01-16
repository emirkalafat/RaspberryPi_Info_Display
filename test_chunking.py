import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Explicitly initialize I2C at 100kHz
i2c = busio.I2C(board.SCL, board.SDA, frequency=100_000)


# Subclass to implement chunked writing
class SSD1306_Chunked(adafruit_ssd1306.SSD1306_I2C):
    def write_framebuf(self):
        # We break the buffer into chunks and prepend 0x40 (Data Mode) to each chunk
        CHUNK_SIZE = 32
        for i in range(0, len(self.buffer), CHUNK_SIZE):
            chunk = self.buffer[i : i + CHUNK_SIZE]
            with self.i2c_device as i2c:
                i2c.write(b"\x40" + chunk)


WIDTH = 128
HEIGHT = 64
oled = SSD1306_Chunked(WIDTH, HEIGHT, i2c, addr=0x3C)

oled.fill(0)
oled.show()

# Draw something
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
draw.text((10, 10), "Chunk Test", fill=0)

oled.image(image)
oled.show()
print("Success!")
