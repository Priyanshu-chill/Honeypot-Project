import joblib

model = joblib.load("model.pkl")

features = [
    "file_size",
    "url_count",
    "domain_count",
    "ip_count",
    "yara_count",
    "string_count",
    "vt_malicious"
]

for f, score in zip(
    features,
    model.feature_importances_
):
    print(f"{f}: {score:.4f}")
