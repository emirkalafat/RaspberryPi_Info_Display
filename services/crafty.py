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
        # 1. Determine Fetch Method
        servers = []
        is_authenticated = bool(self.api_client.token)
        
        try:
            if is_authenticated:
                servers = self.api_client.get_servers()
            else:
                servers = self.api_client.get_public_server_stats()
            
            # Map of server UUID to data
            new_cache = {}
            
            if servers:
                for server in servers:
                    # Handle data structure differences
                    # Authenticated (get_servers) returns basic info, need extra call for stats
                    # Public (get_public_server_stats) returns EVERYTHING in one list
                    
                    uuid = ""
                    stats = {}
                    
                    if is_authenticated:
                        uuid = server.get("server_id")
                        stats = self.api_client.get_server_stats(uuid) or {}
                    else:
                        # Public API returns structure directly
                        uuid = server.get("id") # Public API uses "id"
                        stats = server
                        
                    if not uuid:
                        continue

                    # Common Processing
                    is_running = stats.get("running", False)
                    player_list = []
                    
                    # Player List parsing (Only for Authenticated)
                    if is_running and is_authenticated:
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
                                    
                    # Public API does not provide player names, so list is empty.
                    # We rely on 'online' count.
                    
                    # Normalize Keys
                    # Auth: 'max' -> 'max', 'players' (raw)
                    # Public: 'max', 'online'
                    
                    player_count = 0
                    if is_authenticated:
                        player_count = len(player_list)
                    else:
                        player_count = int(stats.get("online", 0))
                                        
                    new_cache[uuid] = {
                        "is_running": is_running,
                        "max_players": stats.get("max", "0"),
                        "player_count": player_count,
                        "player_names": [str(p) for p in player_list],
                        "version": stats.get("version", ""),
                        "desc": stats.get("desc", ""),
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
