import csv
import json
import os
import subprocess

BASE_DIR = "/home/chill/Honeypot-Project"
ANALYZER_DIR = f"{BASE_DIR}/analysis/static"
DATASET_FILE = f"{BASE_DIR}/ml/dataset/malware_features.csv"


def append_row(report, category):

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

    with open(DATASET_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)


def process_folder(folder_path, category):

    files = os.listdir(folder_path)

    for file in files:

        sample_path = os.path.join(folder_path, file)

        print(f"Processing: {file}")

        subprocess.run(
            [
                "cp",
                sample_path,
                f"{ANALYZER_DIR}/samples/sample"
            ]
        )

        subprocess.run(
    [
        "python3",
        "analyzer.py"
    ],
    cwd=ANALYZER_DIR
)

        report_file = (
            f"{ANALYZER_DIR}/reports/report.json"
        )

        with open(report_file, "r") as f:
            report = json.load(f)

        append_row(report, category)

    print("Completed:", category)


if __name__ == "__main__":

    folder = input("Folder Path: ")
    category = input("Category: ")

    process_folder(folder, category)
