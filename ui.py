import time

class WindowManager:
    def __init__(self, start_screen=0, duration=5, auto_scroll=True):
        self.screens = []
        self.current_screen_index = start_screen
        self.last_switch_time = time.time()
        self.duration = duration
        self.auto_scroll = auto_scroll

    def add_screen(self, screen):
        self.screens.append(screen)

    def next_screen(self):
        self.current_screen_index = (self.current_screen_index + 1) % len(self.screens)
        self.last_switch_time = time.time()

    def update(self):
        """Checks if it's time to switch screens."""
        if self.auto_scroll and len(self.screens) > 1:
            if time.time() - self.last_switch_time > self.duration:
                self.next_screen()

    def draw(self, image, draw):
        """Draws the current screen."""
        if not self.screens:
            draw.text((10, 20), "No Screens", fill=255)
            return

        current_screen = self.screens[self.current_screen_index]
        current_screen.draw(image, draw, self.duration)
