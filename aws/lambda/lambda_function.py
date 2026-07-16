import json
import boto3
import hashlib
import urllib.parse

# Configuration
SQS_QUEUE_URL = "https://sqs.ap-south-1.amazonaws.com/460442982798/malware-analysis-queue"  # paste your queue URL
AWS_REGION = "ap-south-1"

def lambda_handler(event, context):
    print("Lambda triggered!")
    print(f"Event: {json.dumps(event)}")
    
    sqs_client = boto3.client("sqs", region_name=AWS_REGION)
    
    # Get file details from S3 event
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(
            record["s3"]["object"]["key"]
        )
        size = record["s3"]["object"]["size"]
        
        print(f"New file in S3: {key}")
        
        # Extract SHA256 from filename
        filename = key.split("/")[-1]
        
        # Create analysis task
        task = {
            "filename": filename,
            "s3_bucket": bucket,
            "s3_key": key,
            "size_bytes": size,
            "status": "PENDING_ANALYSIS"
        }
        
        # Send to SQS
        response = sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(task)
        )
        
        print(f"✅ Task sent to SQS: {response['MessageId']}")
    
    return {
        "statusCode": 200,
        "body": json.dumps("Task queued successfully!")
    }