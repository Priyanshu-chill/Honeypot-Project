import os
import time
import hashlib
import json
import datetime

# Path where Cowrie saves uploaded malware files
WATCH_DIR = os.path.expanduser(
    "~/Honeypot-Project/honeypot/cowrie/var/lib/cowrie/downloads"
)

def get_file_hash(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def scan_directory():
    if not os.path.exists(WATCH_DIR):
        os.makedirs(WATCH_DIR)
        print(f"Created watch directory: {WATCH_DIR}")

    print("=" * 50)
    print("COWRIE FILE MONITOR STARTED")
    print(f"Watching: {WATCH_DIR}")
    print("=" * 50)

    seen_files = set()

    while True:
        current_files = set(os.listdir(WATCH_DIR))
        new_files = current_files - seen_files

        for filename in new_files:
            filepath = os.path.join(WATCH_DIR, filename)
            file_size = os.path.getsize(filepath)
            file_hash = get_file_hash(filepath)
            timestamp = str(datetime.datetime.now())

            # Create alert
            alert = {
                "timestamp": timestamp,
                "filename": filename,
                "filepath": filepath,
                "size_bytes": file_size,
                "sha256": file_hash,
                "status": "NEW MALWARE DETECTED"
            }

            print("\n🚨 NEW FILE DETECTED!")
            print(json.dumps(alert, indent=4))

            # Save alert to log file
            with open("malware_alerts.json", "a") as f:
                f.write(json.dumps(alert) + "\n")

        seen_files = current_files
        time.sleep(5)

if __name__ == "__main__":
    scan_directory()