import hashlib
import os
import re
import subprocess
import json
import yara
from datetime import datetime
from vt_lookup import lookup_virustotal
import sys

sys.path.append(
    "/home/chill/Honeypot-Project/ml"
)

from predict import predict_category

SAMPLE_FILE = "samples/sample"


def calculate_hashes(filepath):

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as f:

        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
            sha1.update(chunk)
            sha256.update(chunk)

    return {
        "md5": md5.hexdigest(),
        "sha1": sha1.hexdigest(),
        "sha256": sha256.hexdigest()
    }


def get_file_type(filepath):

    result = subprocess.run(
        ["file", filepath],
        capture_output=True,
        text=True
    )

    return result.stdout.strip()


def extract_strings(filepath):

    result = subprocess.run(
        ["strings", filepath],
        capture_output=True,
        text=True
    )

    return result.stdout.splitlines()


def extract_urls(strings):

    pattern = r'https?://[^\s]+'
    urls = []

    for line in strings:
        urls.extend(re.findall(pattern, line))

    return list(set(urls))


def extract_ips(strings):

    pattern = r'(?:\d{1,3}\.){3}\d{1,3}'
    ips = []

    for line in strings:
        ips.extend(re.findall(pattern, line))

    return list(set(ips))


def extract_domains(strings):

    pattern = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
    domains = []

    for line in strings:
        domains.extend(re.findall(pattern, line))

    return list(set(domains))


def run_yara_scan(filepath):

    try:

        rules = yara.compile(
            filepath="rules/suspicious.yar"
        )

        matches = rules.match(filepath)

        return [match.rule for match in matches]

    except Exception as e:

        print(f"YARA Error: {e}")

        return []


def calculate_risk_score(
    urls,
    domains,
    ips,
    yara_hits,
    vt_result
):

    score = 0

    if len(urls) > 0:
        score += 1

    if len(domains) > 0:
        score += 1

    if len(ips) > 0:
        score += 1

    if len(yara_hits) > 0:
        score += 2

    if vt_result.get("vt_found"):

        malicious = vt_result.get(
            "malicious",
            0
        )

        if malicious >= 20:
            score += 5

        elif malicious >= 5:
            score += 3

        elif malicious >= 1:
            score += 1

    if score >= 5:
        return "High"

    elif score >= 2:
        return "Medium"

    else:
        return "Low"

def classify_malware(yara_hits):

    malware_map = {

        "Suspicious_Domain":
            "Generic Downloader"

    }

    for hit in yara_hits:

        if hit in malware_map:
            return malware_map[hit]

    return "Unknown"


def generate_summary(
    malware_family,
    risk_score,
    domains,
    ips,
    yara_hits,
    vt_result
):

    summary = (
        f"The analyzed sample was classified as "
        f"{malware_family}. "
        f"Risk level is {risk_score}. "
    )

    if yara_hits:
        summary += (
            f"YARA Matches: "
            f"{', '.join(yara_hits)}. "
        )

    if domains:
        summary += (
            f"Domains: "
            f"{', '.join(domains)}. "
        )

    if ips:
        summary += (
            f"IPs: "
            f"{', '.join(ips)}. "
        )

    if vt_result.get("vt_found"):

        summary += (
            f"VirusTotal reported "
            f"{vt_result.get('malicious',0)} "
            f"malicious detections. "
        )

        tags = vt_result.get(
            "tags",
            []
        )

        if tags:

            summary += (
                f"Threat Tags: "
                f"{', '.join(tags)}."
            )

    return summary

    if not domains and not ips and not yara_hits:

        return (
            f"The analyzed sample was classified as "
            f"{malware_family}. Risk level is "
            f"{risk_score}. No suspicious domains, "
            f"IPs or YARA signatures were detected."
        )

    return (
        f"The analyzed sample was classified as "
        f"{malware_family}. Risk level is "
        f"{risk_score}. "
        f"YARA Matches: {', '.join(yara_hits)}. "
        f"Domains: {', '.join(domains)}. "
        f"IPs: {', '.join(ips)}."
    )


def get_recommendation(risk_score):

    if risk_score == "High":

        return (
            "Block identified domains and IPs. "
            "Investigate affected hosts immediately."
        )

    elif risk_score == "Medium":

        return (
            "Monitor network activity and "
            "validate indicators."
        )

    else:

        return (
            "No immediate action required."
        )


def analyze(filepath):

    hashes = calculate_hashes(filepath)

    file_type = get_file_type(filepath)

    file_size = os.path.getsize(filepath)

    strings_output = extract_strings(filepath)

    urls = extract_urls(strings_output)

    ips = extract_ips(strings_output)

    domains = extract_domains(strings_output)

    yara_hits = run_yara_scan(filepath)

    vt_result = lookup_virustotal(
        hashes["sha256"]
    )

    risk_score = calculate_risk_score(
        urls,
        domains,
        ips,
        yara_hits,
    vt_result
    )

    malware_family = classify_malware(
        yara_hits
    )

    summary = generate_summary(
        malware_family,
        risk_score,
        domains,
        ips,
        yara_hits,
    vt_result
    )

    recommendation = get_recommendation(
        risk_score
    )

    ml_input = {

       "file_size":
           file_size,

       "urls":
           urls,

       "domains":
           domains,

       "ips":
           ips,

       "yara_hits":
           yara_hits,

       "string_count":
           len(strings_output),

       "virustotal":
           vt_result
    }

    ml_prediction = predict_category(
        ml_input
    )

    report = {

        "analysis_time":
            datetime.utcnow().isoformat() + "Z",

        "md5":
            hashes["md5"],

        "sha1":
            hashes["sha1"],

        "sha256":
            hashes["sha256"],

        "file_size":
            file_size,

        "file_type":
            file_type,

        "urls":
            urls,

        "domains":
            domains,

        "ips":
            ips,

        "yara_hits":
            yara_hits,

        "virustotal":
            vt_result,

        "risk_score":
            risk_score,

        "malware_family":
            malware_family,
    
    "ml_prediction":
            ml_prediction,

        "threat_summary":
            summary,

        "recommended_action":
            recommendation,

        "string_count":
            len(strings_output)
    }

    print(json.dumps(report, indent=4))

    with open(
        "reports/report.json",
        "w"
    ) as f:

        json.dump(
            report,
            f,
            indent=4
        )


if __name__ == "__main__":
    analyze(SAMPLE_FILE)
