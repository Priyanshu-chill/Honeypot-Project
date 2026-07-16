import boto3

EMAIL = "manasgoyal92@gmail.com"

ses = boto3.client(
    "ses",
    region_name="ap-south-1"
)

def send_alert(report):

    subject = (
        f"[{report['risk_score']}] "
        f"Malware Analysis Alert"
    )

    body = f"""
Malware Analysis Report

Risk Score:
{report['risk_score']}

Malware Family:
{report['malware_family']}

ML Prediction:
{report.get('ml_prediction', 'Unknown')}

SHA256:
{report['sha256']}

VirusTotal Detections:
{report.get('virustotal', {}).get('malicious', 0)}

Domains:
{', '.join(report['domains'])}

IPs:
{', '.join(report['ips'])}

Recommended Action:
{report['recommended_action']}

Threat Summary:
{report['threat_summary']}
"""
    response = ses.send_email(
        Source=EMAIL,
        Destination={
            "ToAddresses": [EMAIL]
        },
        Message={
            "Subject": {
                "Data": subject
            },
            "Body": {
                "Text": {
                    "Data": body
                }
            }
        }
    )

    return response

