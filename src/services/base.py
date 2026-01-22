import threading
import time

class BackgroundService:
    def __init__(self, update_interval=60):
        self._data = None
        self._lock = threading.Lock()
        self._last_update = 0
        self._update_interval = update_interval
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _loop(self):
        # Initial wait to let system settle? No, fetch immediately.
        while not self._stop_event.is_set():
            try:
                # Only update if interval passed OR no data yet
                if time.time() - self._last_update >= self._update_interval or self._data is None:
                    new_data = self.fetch_data()
                    if new_data:
                        with self._lock:
                            self._data = new_data
                        self._last_update = time.time()
                        print(f"[{self.__class__.__name__}] Updated Data")
            except Exception as e:
                print(f"[{self.__class__.__name__}] Error: {e}")
            
            # Sleep a bit to prevent tight loop, but check stop event
            time.sleep(1)

    def fetch_data(self):
        """Override this to perform the actual network request."""
        return None

    def get_data(self):
        with self._lock:
            return self._data

    def stop(self):
        self._stop_event.set()
