
import sys
import os
import time

# Allow importing from parent directory
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
import config
from services import CraftyClient, CraftyService

# Disable Warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def verify_hybrid_mode():
    print("--- Starting Verify Hybrid Mode ---")
    
    # 1. Initialize Client
    print(f"Connecting to {config.CRAFTY_URL}")
    client = CraftyClient(config.CRAFTY_URL, config.CRAFTY_USERNAME, config.CRAFTY_PASSWORD)
    
    # 2. Attempt Login (Expect Failure due to 2FA)
    print("Attempting Login...")
    authenticated = client.login()
    print(f"Login Result: {authenticated}")
    
    if authenticated:
        print("WARNING: Login succeeded unexpectedly (maybe 2FA is off?). Verification continues in Auth Mode.")
    else:
        print("Login Failed as expected. Proceeding to Fallback Mode.")
        
    # 3. Initialize Service
    service = CraftyService(client)
    
    # 4. Fetch Servers (Mimic app.py logic)
    print("Fetching Servers List...")
    servers = []
    if authenticated:
        servers = client.get_servers()
    else:
        servers = client.get_public_server_stats()
        
    print(f"Found {len(servers)} servers.")
    if len(servers) > 0:
        print(f"First Server Data Sample (Raw): {servers[0]}")
        
        # Simulate app.py Normalization
        unified_server = {}
        if authenticated:
            unified_server = servers[0]
            if "server_name" not in unified_server and "server_label" in unified_server:
                unified_server["server_name"] = unified_server["server_label"]
        else:
            unified_server = {
                "server_id": servers[0].get("id"),
                "server_name": servers[0].get("world_name", "Unknown Server")
            }
        print(f"Unified Server Data: {unified_server}")
        
        if not unified_server.get("server_id") or not unified_server.get("server_name"):
            print("ERROR: Normalization Failed! Missing ID or Name.")
    else:
        print("ERROR: No servers found even in public mode.")
        return

    # 5. Simulate Service Update Loop
    print("\nSimulating Background Fetch...")
    data = service.fetch_data()
    print("Fetched Data Result:")
    if data:
        for uuid, stats in data.items():
            print(f"UUID: {uuid}")
            print(f"  Running: {stats.get('is_running')}")
            print(f"  Online: {stats.get('player_count')} / {stats.get('max_players')}")
            print(f"  Player Names: {stats.get('player_names')}") # Should be [] in fallback
            
            # Check correctness
            if not authenticated and stats.get('player_names'):
                print("  ERROR: Player names found in fallback mode!")
    else:
        print("ERROR: Service fetch_data returned None")

if __name__ == "__main__":
    verify_hybrid_mode()
