import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

MODEL_PATH = "app/spam_model.pkl"

def train_and_save_model():
    # Load dataset
    df = pd.read_csv("data/smsspam.csv")  # columns: label,text
    texts = df['text']
    labels = df['label']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )

    # Vectorize
    vectorizer = TfidfVectorizer(stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Train multiple classifiers
    classifiers = {
        "MultinomialNB": MultinomialNB(),
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "LinearSVC": LinearSVC(),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42)
    }

    # Ensure best_clf is never None
    best_clf = list(classifiers.values())[0]
    best_score = 0

    for name, clf in classifiers.items():
        clf.fit(X_train_vec, y_train)
        score = clf.score(X_test_vec, y_test)
        print(f"{name} accuracy: {score:.4f}")
        if score > best_score:
            best_score = score
            best_clf = clf
            
    # Evaluate best model
    y_pred = best_clf.predict(X_test_vec)
    print("\nClassification report for best model:")
    print(classification_report(y_test, y_pred))

    # Save vectorizer and best classifier
    with open(MODEL_PATH, "wb") as f:
        pickle.dump((vectorizer, best_clf), f)

def load_model():
    with open(MODEL_PATH, "rb") as f:
        vectorizer, clf = pickle.load(f)
    return vectorizer, clf

def predict(text: str) -> str:
    """
    Predict label for given text.
    Returns the label as a string.
    """
    vectorizer, clf = load_model()
    X = vectorizer.transform([text])
    return clf.predict(X)[0]

def predict_with_prob(text: str):
    """
    Predict label and show probabilities/confidence.
    Works with classifiers that support predict_proba.
    For LinearSVC (no predict_proba), fallback to decision_function.
    """
    vectorizer, clf = load_model()
    X = vectorizer.transform([text])

    # Check if classifier supports predict_proba
    if hasattr(clf, "predict_proba"):
        probs = clf.predict_proba(X)[0]
        labels = clf.classes_
        result = dict(zip(labels, probs))
    else:
        # Fallback: decision_function scaled to 0-1
        if hasattr(clf, "decision_function"):
            import numpy as np
            scores = clf.decision_function(X)
            # For binary classification, convert to pseudo-probabilities
            probs = 1 / (1 + np.exp(-scores))  # sigmoid
            labels = clf.classes_
            # Ensure shape
            if probs.shape == (1,):
                probs = [1 - probs[0], probs[0]]
            result = dict(zip(labels, probs))
        else:
            # fallback to 100% for predicted class
            pred = clf.predict(X)[0]
            result = {pred: 1.0}
    pred_label = clf.predict(X)[0]
    return pred_label, result
