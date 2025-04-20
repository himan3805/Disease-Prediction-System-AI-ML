import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv('medical_data.csv')

# Handle missing values (if any)
df.fillna(method='ffill', inplace=True)

# Encode categorical features
encoder = LabelEncoder()
df['Disease'] = encoder.fit_transform(df['Disease'])

# Feature selection
X = df.drop(columns=['Disease'])
y = df['Disease']

# Encode non-numeric symptoms
for column in X.columns:
    if X[column].dtype == 'object':
        X[column] = LabelEncoder().fit_transform(X[column].astype(str))

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Save processed data
X_train.to_csv('X_train.csv', index=False)
X_test.to_csv('X_test.csv', index=False)
y_train.to_csv('y_train.csv', index=False)
y_test.to_csv('y_test.csv', index=False)

print("✅ Data preprocessing complete!")
