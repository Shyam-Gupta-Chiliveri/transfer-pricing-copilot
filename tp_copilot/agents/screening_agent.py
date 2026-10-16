"""Screen company descriptions against the Härtetechnik Polska profile.

The task is the one TruthLens solved for text: accept or reject a description.
The model here is TF-IDF plus logistic regression so the demo runs without a
GPU. Labels are portfolio labels, not a Big-4 database.
"""

from __future__ import annotations

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, cross_val_score
from sklearn.pipeline import Pipeline

from tp_copilot.data.comparables import COMPANIES

PROFILE = (
    "Limited-risk contract manufacturer of induction-hardened and machined "
    "automotive metal parts. The principal owns the process recipe, the OEM "
    "contract and warranty risk."
)


def _pipeline() -> Pipeline:
    return Pipeline(
        [
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words="english")),
            (
                "clf",
                LogisticRegression(class_weight="balanced", max_iter=400, random_state=42),
            ),
        ]
    )


def _texts_and_labels() -> tuple[list[str], np.ndarray]:
    texts = [company.description for company in COMPANIES]
    labels = np.array([company.label for company in COMPANIES])
    return texts, labels


def evaluate() -> dict:
    texts, labels = _texts_and_labels()
    pipe = _pipeline()
    f1 = cross_val_score(pipe, texts, labels, cv=5, scoring="f1")
    predicted = cross_val_predict(pipe, texts, labels, cv=5)
    rows = []
    for company, guess in zip(COMPANIES, predicted):
        rows.append(
            {
                "name": company.name,
                "label": int(company.label),
                "prediction": int(guess),
                "net_cost_plus": company.net_cost_plus,
                "description": company.description,
            }
        )
    return {
        "profile": PROFILE,
        "f1_mean": float(f1.mean()),
        "f1_folds": [float(value) for value in f1],
        "rows": rows,
    }


def screen_text(description: str) -> dict:
    texts, labels = _texts_and_labels()
    pipe = _pipeline()
    pipe.fit(texts, labels)
    probability = float(pipe.predict_proba([description])[0, 1])
    vectorizer = pipe.named_steps["tfidf"]
    classifier = pipe.named_steps["clf"]
    matrix = vectorizer.transform([description])
    coefficients = classifier.coef_[0]
    weighted = matrix.toarray()[0] * coefficients
    names = np.array(vectorizer.get_feature_names_out())
    positive_index = weighted.argsort()[::-1][:6]
    negative_index = weighted.argsort()[:6]
    reasons_for = [names[i] for i in positive_index if weighted[i] > 0][:5]
    reasons_against = [names[i] for i in negative_index if weighted[i] < 0][:5]
    return {
        "comparable": probability >= 0.5,
        "probability": round(probability, 3),
        "reasons_for": reasons_for,
        "reasons_against": reasons_against,
        "profile": PROFILE,
    }


def accepted_peers() -> list[dict]:
    """Human-accepted contract manufacturers. These are the margin set."""
    return [
        {
            "name": company.name,
            "net_cost_plus": company.net_cost_plus,
            "description": company.description,
        }
        for company in COMPANIES
        if company.label == 1 and company.net_cost_plus is not None
    ]
