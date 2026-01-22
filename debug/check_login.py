import requests
import urllib3
import sys
import os

# Allow importing from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print(f"Testing Login to: {config.CRAFTY_URL}")
print(f"Username: {config.CRAFTY_USERNAME}")
# Don't print password

url = f"{config.CRAFTY_URL}/api/v2/auth/login"
payload = {
    "username": config.CRAFTY_USERNAME,
    "password": config.CRAFTY_PASSWORD
}

try:
    response = requests.post(url, json=payload, verify=False, timeout=5)
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print("Response Data:")
        # Identify if token is present
        if data.get("status") == "ok" and "token" in data.get("data", {}):
            print("LOGIN SUCCESSFUL: Token received.")
            print(f"Token start: {data['data']['token'][:10]}...")
        else:
            print("LOGIN FAILED.")
            print(data)
    except:
        print("Could not parse JSON response.")
        print(response.text[:500])
except Exception as e:
    print(f"Error during request: {e}")
