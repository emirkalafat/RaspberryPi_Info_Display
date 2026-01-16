class BaseScreen:
    def __init__(self, font_main, font_small):
        self.font = font_main
        self.font_small = font_small

    def draw(self, image, draw, duration):
        pass

    def draw_bar(self, draw, x, y, width, height, percent):
        # Draw outline
        draw.rectangle((x, y, x + width, y + height), outline=255, fill=0)
        # Draw fill
        fill_width = int(width * (percent / 100.0))
        if fill_width > 0:
            draw.rectangle((x, y, x + fill_width, y + height), outline=None, fill=255)
