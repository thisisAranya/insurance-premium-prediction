# 🏥 Insurance Premium Category Prediction

A machine learning system that predicts insurance premium categories (Low, Medium, High) using FastAPI backend and Streamlit frontend.

## 🚀 Complete Setup Guide

### Step 1: Prerequisites
- Python 3.8+ installed
- Git installed
- Text editor or IDE

### Step 2: Clone Repository
```bash
git clone https://github.com/thisisAranya/insurance-premium-prediction.git
cd insurance-premium-prediction
```

### Step 3: Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Verify activation (you should see (venv) in your terminal)
```

### Step 4: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

### Step 5: Prepare Your Dataset
```bash
# Place your CSV file as 'insurance_premium_dataset.csv' in the project root
# Your dataset must have these exact columns:
```
Required columns:
```
Age, Gender, Marital_Status, Occupation, Education, Monthly_Income,
Area_Type, BMI, Smoking_Status, Alcohol_Consumption, Physical_Activity_hr_wk,
Sleep_hr_day, Family_History, Preexisting_Condition, Doctor_Visits_Last_Year,
Current_Medications, Stress_Level, Pollution_Exposure, Food_Habit,
Claim_History, Claim_Amount_Last_Year, Insurance_Type, Policy_Tenure,
Premium_Paid_Last_Year, Loyalty_Score, Premium_Category
```

### Step 6: Train the Model (REQUIRED)
```bash
# Train the model with your dataset
python train_model.py

# Expected output:
# ✅ Model saved to insurance_model.pkl
# 🎯 Accuracy: 0.87
# 🔁 Macro F1 Score: 0.85
# ... (classification report and confusion matrix)

# Verify model file creation
# Check that 'insurance_model.pkl' exists in your project folder
```

### Step 7: Start FastAPI Backend
```bash
# Open Terminal 1 and activate environment
cd insurance-premium-prediction
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Start FastAPI server
python app.py

# Expected output:
# ✅ Model loaded successfully!
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 8: Start Streamlit Frontend
```bash
# Open Terminal 2 (keep Terminal 1 running) and activate environment
cd insurance-premium-prediction
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Start Streamlit app
streamlit run streamlit_app.py

# Expected output:
# You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
```

### Step 9: Access the Application
- **Web Interface (Streamlit)**: http://localhost:8501
- **API Documentation (FastAPI)**: http://localhost:8000/docs
- **API Endpoint**: http://localhost:8000/predict

## 📁 Project Structure
```
insurance-premium-prediction/
├── app.py                          # FastAPI backend
├── streamlit_app.py                # Streamlit frontend
├── train_model.py                  # Model training script
├── insurance_premium_dataset.csv   # Your training dataset
├── insurance_model.pkl             # Generated after training
├── requirements.txt                # Dependencies
├── .gitignore                      # Git ignore file
└── README.md                       # This file
```

**Important**: 
- The `insurance_model.pkl` file is NOT included in the repository
- You must train the model first using your own dataset
- This ensures the model is trained on your specific data

## 🎯 Features
- **Custom Model Training**: Train on your own dataset
- **Web Interface**: Easy-to-use form with 25 input fields
- **API**: RESTful API with automatic validation
- **Predictions**: Premium categories with confidence scores
- **Visualizations**: Interactive charts and risk analysis
- **Model**: Random Forest with preprocessing pipeline

## 📝 Input Fields
**Personal Information**: Age, Gender, Marital Status, Occupation, Education, Income, Area Type, Loyalty Score

**Health Information**: BMI, Smoking, Alcohol, Physical Activity, Sleep, Family History, Medical Conditions, Doctor Visits, Current Medications

**Lifestyle & Insurance**: Stress Level, Pollution Exposure, Food Habits, Claim History, Previous Claims, Insurance Type, Policy Details

## 🔧 API Usage Example
```bash
curl -X POST "http://localhost:8000/predict" \
-H "Content-Type: application/json" \
-d '{
  "Age": 31,
  "Gender": "Male",
  "Marital_Status": "Single",
  "Occupation": "Private Job",
  "Education": "Bachelor",
  "Monthly_Income": 80000,
  "Area_Type": "Urban",
  "BMI": 27,
  "Smoking_Status": "Never",
  "Alcohol_Consumption": "Never",
  "Physical_Activity_hr_wk": 3,
  "Sleep_hr_day": 6,
  "Family_History": "Yes",
  "Preexisting_Condition": "None",
  "Doctor_Visits_Last_Year": 2,
  "Current_Medications": 1,
  "Stress_Level": "Low",
  "Pollution_Exposure": "High",
  "Food_Habit": "Mixed",
  "Claim_History": 0,
  "Claim_Amount_Last_Year": 0,
  "Insurance_Type": "Basic",
  "Policy_Tenure": 5,
  "Premium_Paid_Last_Year": 1200,
  "Loyalty_Score": 0.8
}'
```

**Expected Response:**
```json
{
  "premium_category": "Medium",
  "probabilities": {
    "Low": 0.2,
    "Medium": 0.6,
    "High": 0.2
  },
  "confidence": 0.6
}
```

## 🧠 Model Training Details

### Dataset Requirements
Your CSV dataset must include all these columns with exact names:
```
Age, Gender, Marital_Status, Occupation, Education, Monthly_Income,
Area_Type, BMI, Smoking_Status, Alcohol_Consumption, Physical_Activity_hr_wk,
Sleep_hr_day, Family_History, Preexisting_Condition, Doctor_Visits_Last_Year,
Current_Medications, Stress_Level, Pollution_Exposure, Food_Habit,
Claim_History, Claim_Amount_Last_Year, Insurance_Type, Policy_Tenure,
Premium_Paid_Last_Year, Loyalty_Score, Premium_Category
```

### Training Process
The `train_model.py` script performs:

1. **Data Loading & Preprocessing**
   - Loads CSV dataset
   - Cleans column names (lowercase, underscores)
   - Separates features and target variable

2. **Feature Engineering**
   - Identifies numerical vs categorical features
   - Applies StandardScaler to numerical features
   - Applies OneHotEncoder to categorical features

3. **Model Training**
   - Uses Random Forest Classifier with optimized parameters
   - Applies SMOTE for handling class imbalance
   - Performs train-test split (80/20)

4. **Model Evaluation**
   - Calculates accuracy and F1-score
   - Generates classification report
   - Creates confusion matrix

5. **Model Persistence**
   - Saves trained pipeline as `insurance_model.pkl`
   - Includes preprocessor and classifier

### Training Output Example
```
✅ Model saved to insurance_model.pkl
🎯 Accuracy: 0.87
🔁 Macro F1 Score: 0.85
📊 Classification Report:
              precision    recall  f1-score   support
        High       0.84      0.82      0.83       156
         Low       0.89      0.91      0.90       198
      Medium       0.86      0.88      0.87       189
    accuracy                           0.87       543
   macro avg       0.86      0.87      0.87       543
weighted avg       0.87      0.87      0.87       543
```

## 📋 Requirements
```txt
# Web Framework & API
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0

# Frontend & Visualization
streamlit==1.28.0
plotly==5.17.0

# Data Processing & ML
pandas==2.1.3
numpy==1.24.3
scikit-learn==1.3.2
imbalanced-learn==0.11.0

# HTTP Requests
requests==2.31.0

# Serialization
pickle-mixin==1.0.2

# Additional dependencies
python-multipart==0.0.6
python-dotenv==1.0.0
typing-extensions==4.8.0
```

## 🛠 Troubleshooting

### Common Issues & Solutions

**Environment not activated:**
```bash
# Make sure you see (venv) in your terminal
# If not, activate it:
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

**Model not found error:**
```bash
# This error occurs if you haven't trained the model yet
# Solution: Train the model first (REQUIRED)
python train_model.py

# The model file (insurance_model.pkl) is not included in the repository
# You must generate it using your own dataset
```

**API not connecting:**
```bash
# Check if FastAPI is running on port 8000
# Look for this message: "Uvicorn running on http://127.0.0.1:8000"
# If port is busy, kill the process or change port in app.py
```

**Streamlit not loading:**
```bash
# Make sure Streamlit is running on port 8501
# If port conflicts, use:
streamlit run streamlit_app.py --server.port 8502
```

**Dependencies error:**
```bash
# Create fresh virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**Dataset format issues:**
- Ensure CSV has all required columns with exact names
- Check for missing values or incorrect data types
- Verify target column is named 'Premium_Category'
- Check data types match expected format

**Import errors:**
```bash
# Make sure virtual environment is activated
# Reinstall specific packages if needed:
pip install --upgrade fastapi streamlit scikit-learn
```

## 🎮 Testing the System

### 1. Test API Health
```bash
curl http://localhost:8000/health
```

### 2. Test with Sample Data
```bash
curl -X POST http://localhost:8000/test
```

### 3. Test Streamlit Interface
1. Go to http://localhost:8501
2. Fill in sample data
3. Click "Predict Premium Category"
4. Verify results display correctly

## 🔄 Workflow Summary

```
1. Clone Repository
   ↓
2. Setup Virtual Environment
   ↓
3. Install Requirements
   ↓
4. Prepare Dataset
   ↓
5. Train Model (REQUIRED)
   ↓
6. Start FastAPI (Terminal 1)
   ↓
7. Start Streamlit (Terminal 2)
   ↓
8. Use the Application
```

## 📞 Support

### Getting Help
- **GitHub Issues**: Create an issue for bugs or questions
- **Check Logs**: Look at terminal output for error messages
- **Verify Setup**: Follow each step carefully
- **Environment**: Ensure virtual environment is activated

### Common Questions
- **Q**: Can I use my own dataset?
- **A**: Yes! Just ensure it has all required columns

- **Q**: How accurate is the model?
- **A**: Accuracy depends on your dataset quality, typically 85-90%

- **Q**: Can I modify the model parameters?
- **A**: Yes, edit the parameters in `train_model.py`

---

**Made with ❤️ for better insurance decisions**
