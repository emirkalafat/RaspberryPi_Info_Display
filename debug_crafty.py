import config
from crafty import CraftyClient
import json

client = CraftyClient(config.CRAFTY_URL, config.CRAFTY_USERNAME, config.CRAFTY_PASSWORD)
if client.login():
    servers = client.get_servers()
    print(f"Found {len(servers)} servers")
    if servers:
        s = servers[0]
        print("First Server Keys:", s.keys())
        uuid = s.get("server_id")  # Verify this key exists
        print(f"Server UUID: {uuid}")

        if uuid:
            stats = client.get_server_stats(uuid)
            print("\nStats Response:")
            print(json.dumps(stats, indent=2))
        else:
            print("Could not find 'server_uuid' in server object")
            print(json.dumps(s, indent=2))
else:
    print("Login failed")
