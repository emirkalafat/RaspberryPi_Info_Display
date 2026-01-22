import requests
import urllib3

# Suppress insecure request warnings for self-signed certs (localhost)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CraftyClient:
    def __init__(self, url, username, password):
        self.base_url = url.rstrip("/")
        self.username = username
        self.password = password
        self.token = None
        self.session = requests.Session()
        self.session.verify = False  # Trust self-signed certs

    def login(self):
        """Authenticates with the API and retrieves a token."""
        endpoint = f"{self.base_url}/api/v2/auth/login"
        payload = {"username": self.username, "password": self.password}

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "ok":
                self.token = data["data"]["token"]
                # Update session headers with the token
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                print("Crafty Login Successful")
                return True
            else:
                print(f"Crafty Login Failed: {data}")
                return False
        except Exception as e:
            print(f"Crafty Login Error: {e}")
            return False

    def get_servers(self):
        """Retrieves a list of all servers."""
        if not self.token:
            return []

        endpoint = f"{self.base_url}/api/v2/servers"
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            data = response.json()
            if data.get("status") == "ok":
                return data["data"]
            return []
        except Exception as e:
            print(f"Error fetching servers: {e}")
            return []

    def get_server_stats(self, server_uuid):
        """Retrieves stats for a specific server."""
        if not self.token:
            return None

        # Note: The user mentioned /api/v2/servers/{uuid}/stats
        # But depending on V2/V1 implementation details, we might need to adjust.
        # Based on V2 generic docs:
        endpoint = f"{self.base_url}/api/v2/servers/{server_uuid}/stats"
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            data = response.json()
            if data.get("status") == "ok":
                return data["data"]
            return None
        except Exception as e:
            print(f"Error getting stats for {server_uuid}: {e}")
            return None

    def get_public_server_stats(self):
        """Retrieves server stats from the public status endpoint."""
        endpoint = f"{self.base_url}/api/v2/servers/status"
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            data = response.json()
            if data.get("status") == "ok":
                return data["data"]
            return []
        except Exception as e:
            print(f"Error getting public stats: {e}")
            return []
