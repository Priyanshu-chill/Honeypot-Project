import boto3
import json

# SQS Configuration
AWS_REGION = "ap-south-1"
QUEUE_URL = "https://sqs.ap-south-1.amazonaws.com/460442982798/malware-analysis-queue"  # paste your queue URL here

sqs_client = boto3.client("sqs", region_name=AWS_REGION)

# 1. SEND a message to SQS
print("1. Sending message to SQS...")
message = {
    "filename": "evil.elf",
    "sha256": "af8ffed0d1e238d312...",
    "s3_bucket": "honeypot-malware-samples-chill",
    "s3_key": "malware-samples/evil.elf",
    "timestamp": "2026-03-23"
}

response = sqs_client.send_message(
    QueueUrl=QUEUE_URL,
    MessageBody=json.dumps(message)
)
print(f"✅ Message sent! ID: {response['MessageId']}")

# 2. RECEIVE message from SQS
print("\n2. Receiving message from SQS...")
response = sqs_client.receive_message(
    QueueUrl=QUEUE_URL,
    MaxNumberOfMessages=1,
    WaitTimeSeconds=5
)

if "Messages" in response:
    msg = response["Messages"][0]
    body = json.loads(msg["Body"])
    print(f"✅ Message received!")
    print(json.dumps(body, indent=4))

    # 3. DELETE message after processing
    print("\n3. Deleting message from queue...")
    sqs_client.delete_message(
        QueueUrl=QUEUE_URL,
        ReceiptHandle=msg["ReceiptHandle"]
    )
    print("✅ Message deleted!")
else:
    print("No messages in queue")