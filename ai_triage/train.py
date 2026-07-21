import joblib
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline

DATA_PATH = Path(__file__).parent / "data" / "tickets.csv"
MODELS_DIR = Path(__file__).parent / "models"
N_SPLITS = 5


def build_pipeline():
    return Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(max_iter=1000)),
    ])


def evaluate(label, X, y):
    cv = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=42)
    predictions = cross_val_predict(build_pipeline(), X, y, cv=cv)
    print(f"=== {label} (5-fold cross-validation) ===")
    print(classification_report(y, predictions, zero_division=0))


def main():
    df = pd.read_csv(DATA_PATH)
    df["text"] = df["subject"] + " " + df["message"]

    evaluate("Categorie", df["text"], df["category"])
    evaluate("Urgence", df["text"], df["urgency"])

    category_model = build_pipeline()
    category_model.fit(df["text"], df["category"])

    urgency_model = build_pipeline()
    urgency_model.fit(df["text"], df["urgency"])

    MODELS_DIR.mkdir(exist_ok=True)
    joblib.dump(category_model, MODELS_DIR / "category_model.joblib")
    joblib.dump(urgency_model, MODELS_DIR / "urgency_model.joblib")
    print(f"Modeles sauvegardes dans {MODELS_DIR}")


if __name__ == "__main__":
    main()
