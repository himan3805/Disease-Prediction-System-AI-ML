import sqlite3

def store_prediction(name, age, report, predicted_disease):
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            report TEXT NOT NULL,
            predicted_disease TEXT NOT NULL
        )
    """)

    cursor.execute("""
        INSERT INTO Predictions (name, age, report, predicted_disease)
        VALUES (?, ?, ?, ?)
    """, (name, age, report, predicted_disease))

    conn.commit()
    conn.close()