import pandas as pd
import numpy as np
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

# Load dataset
df = pd.read_csv('insurance_premium_dataset.csv')
import pandas as pd

# Assuming df is your DataFrame
for column in df.columns:
    unique_values = df[column].unique()
    print(f"Unique values in '{column}': {unique_values}\n")

# Rename columns for consistency
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Target column
target = 'premium_category'

# Separate features and target
X = df.drop(columns=[target])
y = df[target]

# Identify feature types
categorical = X.select_dtypes(include=['object']).columns.tolist()
numerical = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

# Preprocessor
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numerical),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical)
])

# Define pipeline with SMOTE
pipeline = ImbPipeline([
    ('preprocessor', preprocessor),
    ('smote', SMOTE(random_state=42)),
    ('classifier', RandomForestClassifier(
        n_estimators=300,
        max_depth=20,
        min_samples_split=3,
        min_samples_leaf=2,
        class_weight='balanced_subsample',
        random_state=42
    ))
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Train model
pipeline.fit(X_train, y_train)

# Predict
y_pred = pipeline.predict(X_test)

# Save model
model_path = 'insurance_model.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(pipeline, f)

# Evaluation
accuracy = accuracy_score(y_test, y_pred)
macro_f1 = f1_score(y_test, y_pred, average='macro')

print(f"✅ Model saved to {model_path}")
print(f"🎯 Accuracy: {accuracy:.2f}")
print(f"🔁 Macro F1 Score: {macro_f1:.2f}")
print("📊 Classification Report:")
print(classification_report(y_test, y_pred))
print("🧮 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))