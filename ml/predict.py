import json
import joblib
import pandas as pd

MODEL = joblib.load(
    "/home/chill/Honeypot-Project/ml/model.pkl"
)

def predict_category(report):

    features = pd.DataFrame(
        [[
            report["file_size"],
            len(report["urls"]),
            len(report["domains"]),
            len(report["ips"]),
            len(report["yara_hits"]),
            report["string_count"],
            report["virustotal"].get(
                "malicious",
                0
            )
        ]],
        columns=[
            "file_size",
            "url_count",
            "domain_count",
            "ip_count",
            "yara_count",
            "string_count",
            "vt_malicious"
        ]
    )

    prediction = MODEL.predict(features)

    return prediction[0]


if __name__ == "__main__":

    REPORT_FILE = (
        "../analysis/static/reports/report.json"
    )

    with open(REPORT_FILE) as f:
        report = json.load(f)

    print(
        predict_category(report)
    )
