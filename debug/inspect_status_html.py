import requests
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://localhost:8443/status"

try:
    response = requests.get(url, verify=False)
    html = response.text
    print(f"HTML Length: {len(html)}")
    
    # Check for known server names or patterns if we had them, 
    # but since I don't know the server names, I'll look for common structures.
    # The current code expects 'stats.get("running")' etc.
    
    # Let's print any JSON-like structures found in script tags
    scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
    for script in scripts:
        if "server" in script or "data" in script:
            print("Found suspicious script:")
            print(script[:500])
            
    # Check for simple server count or list
    if "servers" in html:
        print("Found 'servers' in HTML")
        
    # Just print the body content to see if it's empty (SPA) or full (SSR)
    body_content = re.search(r'<body.*?>(.*?)</body>', html, re.DOTALL)
    if body_content:
        content = body_content.group(1)
        print("Body content preview:")
        print(re.sub(r'\s+', ' ', content)[:500])
        
except Exception as e:
    print(f"Error: {e}")
