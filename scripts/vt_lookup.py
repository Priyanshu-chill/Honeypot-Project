import os
import requests
import json

API_KEY = os.getenv("VT_API_KEY")

SHA256 = "3395856ce81f2b7382dee72602f798b642f14140c2ffc2f06d99f0c9aa0d0f5f"

url = f"https://www.virustotal.com/api/v3/files/{SHA256}"

headers = {
    "x-apikey": API_KEY
}

response = requests.get(
    url,
    headers=headers
)

print("Status Code:", response.status_code)

print(
    json.dumps(
        response.json(),
        indent=4
    )
)
