import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "predictions.db"

# Fetch all stored predictions
def fetch_predictions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Predictions ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()
    return records

# Delete selected record
def delete_selected():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("⚠️ Warning", "Please select a record to delete.")
        return

    values = tree.item(selected, "values")
    record_id = values[0]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Predictions WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("✅ Deleted", "Record deleted successfully.")
    refresh_tree()

# Refresh table
def refresh_tree():
    tree.delete(*tree.get_children())
    for row in fetch_predictions():
        tree.insert("", tk.END, values=row)

# Search function
def search_predictions():
    query = search_entry.get().strip()
    if not query:
        refresh_tree()
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Predictions WHERE name LIKE ? OR predicted_disease LIKE ?", 
                   (f"%{query}%", f"%{query}%"))
    results = cursor.fetchall()
    conn.close()

    tree.delete(*tree.get_children())
    for row in results:
        tree.insert("", tk.END, values=row)

# --- GUI Setup ---
root = tk.Tk()
root.title("📋 View Stored Predictions")
root.geometry("800x450")
root.configure(bg="#f9fbff")

title = tk.Label(root, text="📋 Stored Disease Predictions", font=("Segoe UI", 16, "bold"), bg="#f9fbff")
title.pack(pady=10)

# Search Bar
search_frame = ttk.Frame(root)
search_frame.pack(pady=5)

search_entry = ttk.Entry(search_frame, width=40)
search_entry.pack(side="left", padx=5)

search_btn = ttk.Button(search_frame, text="Search", command=search_predictions)
search_btn.pack(side="left", padx=5)

# Table
columns = ("ID", "Name", "Age", "Medical Report", "Predicted Disease")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=140)

tree.pack(pady=10, fill="both", expand=True)

# Buttons
btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="🔁 Refresh", command=refresh_tree).pack(side="left", padx=10)
ttk.Button(btn_frame, text="❌ Delete Selected", command=delete_selected).pack(side="left", padx=10)

# Load data initially
refresh_tree()

# Run the app
root.mainloop()
