# Cloud-Integrated Honeypot and Automated Malware Analysis Platform

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue">
  <img src="https://img.shields.io/badge/AWS-S3%20%7C%20Lambda%20%7C%20SQS%20%7C%20SES-orange">
  <img src="https://img.shields.io/badge/Docker-Container-blue">
  <img src="https://img.shields.io/badge/Kubernetes-Orchestration-326CE5">
  <img src="https://img.shields.io/badge/Cowrie-Honeypot-success">
  <img src="https://img.shields.io/badge/License-MIT-green">
</p>

---

# Overview

This project implements a cloud-native automated malware collection and analysis platform using a Cowrie SSH honeypot integrated with AWS cloud services.

The platform captures attacker activity, automatically detects uploaded malware samples, stores them in Amazon S3, triggers cloud-based processing using AWS Lambda and Amazon SQS, performs malware analysis inside isolated Docker containers, enriches findings using VirusTotal and YARA, classifies malware using Machine Learning, and finally generates structured reports with automated email notifications.

The primary objective is to automate malware triage and reduce manual analyst effort while providing a scalable architecture suitable for cloud environments.

---

# Features

- Cowrie SSH Honeypot
- Brute-force attack logging
- Command execution logging
- SCP/SFTP malware upload detection
- Automatic malware collection
- AWS S3 integration
- AWS Lambda event processing
- Amazon SQS message queue
- Docker-based malware analysis
- File hashing (MD5, SHA1, SHA256)
- File type identification
- IOC extraction
- URL extraction
- Domain extraction
- IP extraction
- YARA rule matching
- VirusTotal enrichment
- Machine Learning malware classification
- Risk scoring
- JSON report generation
- AWS SES email alerts

---

# Architecture

```text
                 Internet
                      │
               Attacker Machine
                      │
                      ▼
             Cowrie SSH Honeypot
                      │
      Captures Login Attempts & Commands
                      │
           Malware Uploaded via SCP
                      │
                      ▼
              monitor.py (Python)
                      │
             Upload Sample to AWS S3
                      │
                      ▼
                 Amazon S3 Bucket
                      │
          S3 Event → AWS Lambda Trigger
                      │
                      ▼
                Amazon SQS Queue
                      │
                      ▼
            analysis_worker.py
                      │
         Download Malware Sample
                      │
                      ▼
        Docker Malware Analysis Engine
                      │
        ┌────────────────────────────┐
        │ SHA256 / MD5 / SHA1        │
        │ File Type Detection        │
        │ Strings Extraction         │
        │ IOC Extraction             │
        │ URL & Domain Detection     │
        │ YARA Scan                  │
        │ VirusTotal Lookup          │
        │ ML Classification          │
        │ Risk Score                 │
        └────────────────────────────┘
                      │
                      ▼
             report.json Generated
                      │
                      ▼
          AWS SES Email Notification
```

---

# Workflow

1. Attacker connects to the Cowrie Honeypot.
2. Login attempts and commands are recorded.
3. Malware is uploaded using SCP/SFTP.
4. Cowrie stores the uploaded sample.
5. monitor.py detects the new file.
6. SHA256 hash is generated.
7. Sample is uploaded to Amazon S3.
8. Lambda is triggered.
9. Lambda publishes an SQS message.
10. analysis_worker.py retrieves the message.
11. Sample is downloaded from S3.
12. Docker analyzer performs malware analysis.
13. VirusTotal enriches the threat intelligence.
14. YARA scans the sample.
15. Random Forest classifier predicts malware category.
16. Risk score is calculated.
17. JSON report is generated.
18. AWS SES sends an automated email alert.

---

# Technology Stack

## Cloud

- AWS S3
- AWS Lambda
- Amazon SQS
- AWS SES

## Malware Analysis

- Python
- Docker
- YARA
- VirusTotal API

## Honeypot

- Cowrie

## Machine Learning

- Scikit-Learn
- Random Forest

## Container Orchestration

- Kubernetes

---

# Project Structure

```
Honeypot-Project/

analysis/
aws/
docker/
honeypot/
kubernetes/
ml/
scripts/
docs/
screenshots/

README.md
requirements.txt
LICENSE
```

---

# Machine Learning

The platform includes a machine learning pipeline that extracts static malware features and trains a Random Forest classifier.

### Malware Categories

- Trojan
- Downloader
- Ransomware
- Benign

### Features Used

- File Size
- String Count
- URL Count
- Domain Count
- IP Count
- VirusTotal Detection Count
- YARA Detection Count

---

# Installation

```bash
git clone https://github.com/<YOUR_USERNAME>/Honeypot-Project.git

cd Honeypot-Project

pip install -r requirements.txt
```

---

# Running the Project

## Start Cowrie

```bash
cd honeypot/cowrie

source cowrie-env/bin/activate

./cowrie-env/bin/cowrie start
```

---

## Start File Monitor

```bash
cd scripts

python3 monitor.py
```

---

## Start Analysis Worker

```bash
cd scripts

python3 analysis_worker.py
```

---

# Sample Analysis

The Docker-based analysis engine performs:

- File hashing
- Static string extraction
- IOC extraction
- URL extraction
- Domain extraction
- IP extraction
- YARA scanning
- VirusTotal enrichment
- Malware classification
- Risk scoring

---


---

# Future Enhancements

- Dynamic malware analysis
- MITRE ATT&CK mapping
- Cyber Kill Chain mapping
- Multi-node Kubernetes deployment
- GitHub Actions CI/CD
- Trivy integration
- Semgrep integration
- Automated security scanning dashboard

---

# Disclaimer

This project is intended for educational and research purposes only.

Malware binaries are intentionally excluded from this repository for safety. The repository includes the malware analysis pipeline, feature engineering code, machine learning model, and dataset generation workflow.

---

# Author

**Priyanshu Goyal**

M.Tech Cybersecurity | National Forensic Sciences University (NFSU)

Cloud Security • Malware Analysis • Threat Detection • AWS • Docker • Kubernetes • Machine Learning
