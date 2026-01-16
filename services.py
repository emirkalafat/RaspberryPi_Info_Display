import psutil
import subprocess
import ast

class SystemMonitorService:
    def get_stats(self):
        """Returns a dict with ip, cpu, ram, temp."""
        return {
            "ip": self._get_ip_address(),
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "temp": self._get_cpu_temp()
        }

    def _get_ip_address(self):
        try:
            cmd = "hostname -I | cut -d' ' -f1"
            return subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
        except:
            return "No IP"

    def _get_cpu_temp(self):
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                temp = float(f.read()) / 1000.0
            return temp
        except:
            return 0.0

class CraftyService:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_server_status(self, server_uuid):
        """Fetches and parses stats for a server, returning a clean object."""
        stats = self.api_client.get_server_stats(server_uuid)
        if not stats:
            return None
        
        is_running = stats.get("running", False)
        player_list = []
        
        if is_running:
            players_raw = stats.get("players", "0")
            if isinstance(players_raw, list):
                player_list = players_raw
            elif isinstance(players_raw, str):
                if players_raw == "False":
                    player_list = []
                elif players_raw.startswith("["):
                    try:
                        player_list = ast.literal_eval(players_raw)
                    except:
                        player_list = []
        
        return {
            "is_running": is_running,
            "max_players": stats.get("max", "0"),
            "player_count": len(player_list),
            "player_names": [str(p) for p in player_list]
        }
