import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, ConfusionMatrixDisplay
import joblib
import datetime

# Load and clean data
df = pd.read_csv("Enron_Emails.csv")
df_cleaned = df.dropna(subset=["body", "label"]).copy()
df_cleaned["body"] = df_cleaned["body"].str.strip()
df_cleaned["label"] = df_cleaned["label"].str.strip()

# Relabeling logic
def relabel_inboxai(text):
    text = text.lower()
    if any(word in text for word in ["win", "free", "prize", "gift", "click", "claim"]):
        return "Spam"
    elif any(word in text for word in [
        "meeting", "report", "project", "invoice", "update",
        "deadline", "filing", "review", "client"
    ]):
        return "Business"
    else:
        return "Personal"

df_cleaned["label"] = df_cleaned["body"].apply(relabel_inboxai)

# Train-test split
X = df_cleaned["body"]
y = df_cleaned["label"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Build pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', max_df=0.95)),
    ('clf', LogisticRegression(max_iter=1000, class_weight='balanced'))
])

# Train model
pipeline.fit(X_train, y_train)

# Evaluate
y_pred = pipeline.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("\nInboxAI - Email Classifier (Spam | Business | Personal)")
print(f"Date trained: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"\nAccuracy: {acc:.3f}")
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred, zero_division=0))

# Save model
joblib.dump(pipeline, "inboxai_model.pkl")
print("✅ Model saved to inboxai_model.pkl")

# Save predictions
results_df = pd.DataFrame({
    "email_text": X_test,
    "true_label": y_test,
    "predicted_label": y_pred
})
results_df.to_csv("inboxai_test_predictions.csv", index=False)
print("📁 Test predictions saved to inboxai_test_predictions.csv")

# Confirmation
print("🎉 Training complete! You’re ready to run the app.")
