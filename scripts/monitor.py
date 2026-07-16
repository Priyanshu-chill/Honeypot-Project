import os
import time
import hashlib
import json
import datetime
import boto3

# AWS Configuration
S3_BUCKET = "honeypot-malware-samples-chill"
AWS_REGION = "ap-south-1"
QUEUE_URL = (
    "https://sqs.ap-south-1.amazonaws.com/"
    "460442982798/malware-analysis-queue"
)

sqs = boto3.client(
    "sqs",
    region_name=AWS_REGION
)

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

def upload_to_s3(filepath, filename, file_hash):
    try:
        s3_client = boto3.client("s3", region_name=AWS_REGION)
        s3_key = f"malware-samples/{file_hash}_{filename}"
        s3_client.upload_file(filepath, S3_BUCKET, s3_key)
        print(f"✅ Uploaded to S3: {s3_key}")
        return s3_key
    except Exception as e:
        print(f"❌ S3 upload failed: {e}")
        return None

def send_sqs_message(s3_key):

    try:

        message = {
            "s3_bucket": S3_BUCKET,
            "s3_key": s3_key
        }

        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(message)
        )

        print(
            f"✅ SQS Message Sent: {s3_key}"
        )

    except Exception as e:

        print(
            f"❌ SQS Error: {e}"
        )

def scan_directory():
    if not os.path.exists(WATCH_DIR):
        os.makedirs(WATCH_DIR)
        print(f"Created watch directory: {WATCH_DIR}")

    print("=" * 50)
    print("COWRIE FILE MONITOR STARTED")
    print(f"Watching: {WATCH_DIR}")
    print(f"S3 Bucket: {S3_BUCKET}")
    print("=" * 50)

    seen_files = set(os.listdir(WATCH_DIR))

    while True:
        current_files = set(os.listdir(WATCH_DIR))
        new_files = current_files - seen_files

        for filename in new_files:
            if filename == ".gitignore":
                 continue
            filepath = os.path.join(WATCH_DIR, filename)
            file_size = os.path.getsize(filepath)
            file_hash = get_file_hash(filepath)
            timestamp = str(datetime.datetime.now())

            print("\n🚨 NEW FILE DETECTED!")
            print(f"Filename: {filename}")
            print(f"Size: {file_size} bytes")
            print(f"SHA256: {file_hash}")

            # Upload to S3
            s3_key = upload_to_s3(
            filepath,
            filename,
            file_hash
            )

            if s3_key:

                send_sqs_message(
                    s3_key
                )

            # Create alert
            alert = {
                "timestamp": timestamp,
                "filename": filename,
                "filepath": filepath,
                "size_bytes": file_size,
                "sha256": file_hash,
                "s3_bucket": S3_BUCKET,
                "s3_key": s3_key,
                "status": "UPLOADED TO S3"
            }

            print(json.dumps(alert, indent=4))

            # Save alert to log file
            with open("malware_alerts.json", "a") as f:
                f.write(json.dumps(alert) + "\n")

        seen_files = current_files
        time.sleep(5)

if __name__ == "__main__":
    scan_directory()
