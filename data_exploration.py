import pandas as pd

# Load the dataset
df = pd.read_csv('medical_data.csv')

# Display basic information
print("📊 Dataset Overview:")
print(df.info())

# Display first few rows
print("\n🔹 Sample Data:")
print(df.head())

# Check for missing values
print("\n❗ Missing Values:")
print(df.isnull().sum())

# Display unique diseases
print("\n🦠 Unique Diseases:")
print(df['Disease'].unique())
