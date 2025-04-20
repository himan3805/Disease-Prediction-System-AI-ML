import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
data_path = "medical_data.csv"  # Use the new dataset
df = pd.read_csv(data_path)

# Ensure dataset contains required columns
if 'Disease' not in df.columns or 'Medical_Report' not in df.columns:
    raise ValueError("Dataset must contain 'Disease' and 'Medical_Report' columns!")

# Text Vectorization (TF-IDF)
vectorizer = TfidfVectorizer(max_features=5000)  # Convert medical report text to numerical features
X = vectorizer.fit_transform(df['Medical_Report'])

# Encode Disease Labels
disease_labels = df['Disease'].unique()  # Get unique disease names
disease_to_index = {disease: i for i, disease in enumerate(disease_labels)}
index_to_disease = {i: disease for disease, i in disease_to_index.items()}
y = df['Disease'].map(disease_to_index)  # Convert disease names to numerical labels

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate Model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Save Model & Vectorizer
with open("disease_prediction_model.pkl", "wb") as file:
    pickle.dump(model, file)

with open("vectorizer.pkl", "wb") as file:
    pickle.dump(vectorizer, file)

with open("disease_mapping.pkl", "wb") as file:
    pickle.dump(index_to_disease, file)

print("Model training completed and saved successfully!")
