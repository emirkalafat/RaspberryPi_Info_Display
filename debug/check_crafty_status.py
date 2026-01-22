import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://localhost:8443/api/v2/servers/status"

print(f"Testing {url}...")
try:
    response = requests.get(url, verify=False, timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("JSON Found!")
        print(json.dumps(data, indent=2))
    else:
        print("Failed to get 200 OK")
        print(response.text[:500])
except Exception as e:
    print(f"Error: {e}")
