import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

DATASET = "dataset/malware_features.csv"

df = pd.read_csv(DATASET)

X = df[
    [
        "file_size",
        "url_count",
        "domain_count",
        "ip_count",
        "yara_count",
        "string_count",
        "vt_malicious"
    ]
]

y = df["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("\nAccuracy:")
print(accuracy_score(y_test, predictions))

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions
    )
)

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        predictions
    )
)

joblib.dump(
    model,
    "model.pkl"
)

print("\nModel Saved: model.pkl")
