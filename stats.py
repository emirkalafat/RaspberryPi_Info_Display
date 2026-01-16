import time
import subprocess
import board
import busio
import psutil
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Create the I2C interface at 100kHz
i2c = busio.I2C(board.SCL, board.SDA, frequency=100_000)

WIDTH = 128
HEIGHT = 64


class SSD1306_Chunked(adafruit_ssd1306.SSD1306_I2C):
    def write_framebuf(self):
        CHUNK_SIZE = 32
        for i in range(0, len(self.buffer), CHUNK_SIZE):
            chunk = self.buffer[i : i + CHUNK_SIZE]
            with self.i2c_device as i2c:
                i2c.write(b"\x40" + chunk)


oled = SSD1306_Chunked(WIDTH, HEIGHT, i2c, addr=0x3C)

# Attempt to load a nicer font
try:
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font = ImageFont.truetype(font_path, 10)
    font_header = ImageFont.truetype(font_path, 11)
except IOError:
    font = ImageFont.load_default()
    font_header = ImageFont.load_default()


def get_ip_address():
    try:
        cmd = "hostname -I | cut -d' ' -f1"
        return subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
    except:
        return "No IP"


def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = float(f.read()) / 1000.0
        return temp
    except:
        return 0.0


def draw_bar(draw, x, y, width, height, percent):
    # Draw outline
    draw.rectangle((x, y, x + width, y + height), outline=255, fill=0)
    # Draw fill
    fill_width = int(width * (percent / 100.0))
    if fill_width > 0:
        draw.rectangle((x, y, x + fill_width, y + height), outline=None, fill=255)


print("Enhanced Stats Display running... Press Ctrl+C to exit.")

try:
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    while True:
        draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

        # 1. Header: IP Address
        ip = get_ip_address()
        # Center the IP
        bbox = font_header.getbbox(ip)
        text_width = bbox[2] - bbox[0]
        x_pos = (WIDTH - text_width) // 2
        draw.text((x_pos, 0), ip, font=font_header, fill=255)

        # Separator line
        draw.line((0, 13, WIDTH, 13), fill=255)

        # 2. Stats
        # CPU
        cpu = psutil.cpu_percent()
        draw.text((0, 16), "CPU", font=font, fill=255)
        draw_bar(draw, 30, 18, 55, 8, cpu)
        draw.text((90, 16), f"{int(cpu)}%", font=font, fill=255)

        # RAM
        ram = psutil.virtual_memory().percent
        draw.text((0, 30), "RAM", font=font, fill=255)
        draw_bar(draw, 30, 32, 55, 8, ram)
        draw.text((90, 30), f"{int(ram)}%", font=font, fill=255)

        # Temp
        temp = get_cpu_temp()
        draw.text((0, 46), f"Temp: {temp:.1f} C", font=font_header, fill=255)

        # Display
        oled.image(image)
        oled.show()

        time.sleep(2)

except KeyboardInterrupt:
    oled.fill(0)
    oled.show()
    print("Exited.")
