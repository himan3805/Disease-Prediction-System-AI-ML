import tkinter as tk
from tkinter import messagebox
import pickle
import numpy as np
from database_manager import store_prediction  # 👈 Import the database saving function

# Load trained model and vectorizer
with open("disease_prediction_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("disease_mapping.pkl", "rb") as f:
    index_to_disease = pickle.load(f)  # {0: "Asthma", 1: "Diabetes", ...}

# GUI Setup
root = tk.Tk()
root.title("🩺 Disease Prediction System")
root.geometry("600x550")
root.configure(bg="#f0f9ff")

LABEL_FONT = ("Segoe UI", 12)
ENTRY_FONT = ("Segoe UI", 11)

# Input fields
tk.Label(root, text="👤 Name", font=LABEL_FONT, bg="#f0f9ff").pack(pady=(15, 0))
entry_name = tk.Entry(root, font=ENTRY_FONT, width=40)
entry_name.pack(pady=5)

tk.Label(root, text="🎂 Age", font=LABEL_FONT, bg="#f0f9ff").pack(pady=(10, 0))
entry_age = tk.Entry(root, font=ENTRY_FONT, width=40)
entry_age.pack(pady=5)

tk.Label(root, text="📝 Medical Report", font=LABEL_FONT, bg="#f0f9ff").pack(pady=(10, 0))
text_report = tk.Text(root, height=10, width=60, font=ENTRY_FONT)
text_report.pack(pady=10)

# Result label
result_label = tk.Label(root, text="", font=("Segoe UI", 13, "bold"), fg="green", bg="#f0f9ff")
result_label.pack(pady=10)

# Predict button function
def predict_disease():
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    report = text_report.get("1.0", tk.END).strip()

    if not name or not age or not report:
        messagebox.showwarning("Input Missing", "Please fill all the fields.")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Invalid Age", "Please enter a valid age (number).")
        return

    # Vectorize and predict
    report_vector = vectorizer.transform([report])
    prediction = model.predict(report_vector)[0]
    predicted_disease = index_to_disease.get(prediction, "Unknown")

    # Show prediction
    result_label.config(text=f"✅ Predicted Disease: {predicted_disease}")

    # Store in database
    try:
        store_prediction(name, age, report, predicted_disease)
    except Exception as e:
        messagebox.showerror("Database Error", f"Could not store prediction:\n{e}")

# Predict Button
tk.Button(root, text="🔍 Predict Disease", command=predict_disease,
          font=("Segoe UI", 12), bg="#007acc", fg="white", width=20).pack(pady=15)

# Run the app
root.mainloop()
