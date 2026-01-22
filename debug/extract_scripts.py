import requests
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://localhost:8443/status"

try:
    response = requests.get(url, verify=False)
    html = response.text
    
    scripts = re.findall(r'<script.*?>(.*?)</script>', html, re.DOTALL)
    
    with open("debug/status_scripts.js", "w") as f:
        for i, script in enumerate(scripts):
            f.write(f"// Script {i}\n")
            f.write(script)
            f.write("\n\n")
            
    print("Scripts extracted to debug/status_scripts.js")
        
except Exception as e:
    print(f"Error: {e}")
