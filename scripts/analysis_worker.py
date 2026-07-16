import boto3
import json
import os
import subprocess
import shutil

from email_alert import send_alert

AWS_REGION = "ap-south-1"

QUEUE_URL = (
    "https://sqs.ap-south-1.amazonaws.com/"
    "460442982798/malware-analysis-queue"
)

DOWNLOAD_DIR = "./downloads"
ANALYZER_INPUT = "./analyzer_input"
ANALYZER_REPORTS = "./analyzer_reports"

sqs = boto3.client(
    "sqs",
    region_name=AWS_REGION
)

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)

os.makedirs(
    DOWNLOAD_DIR,
    exist_ok=True
)

os.makedirs(
    ANALYZER_INPUT,
    exist_ok=True
)

os.makedirs(
    ANALYZER_REPORTS,
    exist_ok=True
)

print("Analysis Worker Started...")

while True:

    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )

    if "Messages" not in response:

        print("No messages found...")
        continue

    message = response["Messages"][0]

    body = json.loads(
        message["Body"]
    )

    print("\nReceived Task:")
    print(
        json.dumps(
            body,
            indent=4
        )
    )

    bucket = body["s3_bucket"]
    key = body["s3_key"]

    filename = key.split("/")[-1]

    local_file = os.path.join(
        DOWNLOAD_DIR,
        filename
    )

    try:

        print(
            f"Downloading {filename}..."
        )

        s3.download_file(
            bucket,
            key,
            local_file
        )

        print(
            "Download Complete."
        )

        print(
            "Preparing Analyzer Input..."
        )

        shutil.copy(
            local_file,
            os.path.join(
                ANALYZER_INPUT,
                "sample"
            )
        )

        print(
            "Launching Static Analyzer..."
        )

        subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "-e",
                f"VT_API_KEY={os.getenv('VT_API_KEY')}",
                "-v",
                f"{os.getcwd()}/analyzer_input:/analysis/samples",
                "-v",
                f"{os.getcwd()}/analyzer_reports:/analysis/reports",
                "static-analyzer"
            ]
        )

        print(
            "Analysis Complete."
        )

        report_file = (
            "./analyzer_reports/report.json"
        )

        if os.path.exists(
            report_file
        ):

            print(
                "\nGenerated Report:"
            )

            with open(
                report_file
            ) as f:

                report = json.load(f)

            print(
                json.dumps(
                    report,
                    indent=4
                )
            )

            try:

                send_alert(
                    report
                )

                print(
                    "Email Alert Sent."
                )

            except Exception as email_error:

                print(
                    f"Email Error: {email_error}"
                )

        receipt_handle = (
            message["ReceiptHandle"]
        )

        sqs.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=receipt_handle
        )

        print(
            "Message Deleted."
        )

    except Exception as e:

        print(
            f"Error: {e}"
        )
