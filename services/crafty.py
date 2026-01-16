import ast
from .base import BackgroundService

class CraftyService(BackgroundService):
    def __init__(self, api_client):
        self.api_client = api_client
        # Update every 30 seconds for Crafty to keep it snappy but not crazy
        super().__init__(update_interval=30)
        self.server_stats_cache = {}
        # We need the list of servers to know what to fetch.
        self.servers = [] 
        
    def fetch_data(self):
        # 1. Get List of Servers
        try:
            servers = self.api_client.get_servers()
            self.servers = servers
            
            # 2. Fetch stats for each
            new_cache = {}
            if servers:
                for server in servers:
                    uuid = server.get("server_id")
                    stats = self.api_client.get_server_stats(uuid)
                    if stats:
                        # Process stats like before
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
                                        
                        new_cache[uuid] = {
                            "is_running": is_running,
                            "max_players": stats.get("max", "0"),
                            "player_count": len(player_list),
                            "player_names": [str(p) for p in player_list],
                        }
            return new_cache
        except Exception as e:
            print(f"Crafty Background Fetch Error: {e}")
            return None

    def get_server_status(self, server_uuid):
        """Returns cached stats for a server."""
        data = self.get_data() # From parent, thread-safe
        if data:
            return data.get(server_uuid)
        return None
