import csv
import json
import os

CSV_FILE = "dataset/malware_features.csv"

def add_report(report_file, category):

    with open(report_file, "r") as f:
        report = json.load(f)

    row = [
        report.get("file_size", 0),
        len(report.get("urls", [])),
        len(report.get("domains", [])),
        len(report.get("ips", [])),
        len(report.get("yara_hits", [])),
        report.get("string_count", 0),
        report.get("virustotal", {}).get("malicious", 0),
        category
    ]

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

    print("Added:", category)

if __name__ == "__main__":

    report_path = input("Report path: ")
    category = input("Category: ")

    add_report(report_path, category)
