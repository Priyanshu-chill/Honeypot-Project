import os
import requests

API_KEY = os.getenv("VT_API_KEY")

def lookup_virustotal(sha256):

    url = f"https://www.virustotal.com/api/v3/files/{sha256}"

    headers = {
        "x-apikey": API_KEY
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        if response.status_code != 200:

            return {
                "vt_found": False
            }

        data = response.json()

        attributes = data["data"]["attributes"]

        stats = attributes.get(
            "last_analysis_stats",
            {}
        )

        return {
            "vt_found": True,
            "malicious":
                stats.get("malicious", 0),

            "suspicious":
                stats.get("suspicious", 0),

            "harmless":
                stats.get("harmless", 0),

            "undetected":
                stats.get("undetected", 0),

            "reputation":
                attributes.get(
                    "reputation",
                    0
                ),

            "tags":
                attributes.get(
                    "tags",
                    []
                )
        }

    except Exception as e:

        return {
            "vt_found": False,
            "error": str(e)
        }
