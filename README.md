# 🏥 Insurance Premium Category Prediction

A machine learning system that predicts insurance premium categories (Low, Medium, High) using FastAPI backend and Streamlit frontend.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation
```bash
# Clone repository
git clone <repository-url>
cd insurance-premium-prediction

# Install dependencies
pip install fastapi uvicorn streamlit requests plotly pandas scikit-learn imbalanced-learn

# Ensure you have the trained model file
# insurance_model.pkl should be in the project root
```

### Run the Application
```bash
# Terminal 1 - Start FastAPI backend
python app.py

# Terminal 2 - Start Streamlit frontend  
streamlit run streamlit_app.py
```

### Access the Application
- **Web Interface**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Endpoint**: http://localhost:8000/predict

## 📁 Project Structure
```
project/
├── app.py              # FastAPI backend
├── streamlit_app.py    # Streamlit frontend
├── train_model.py      # Model training script
├── insurance_model.pkl # Trained model
└── README.md          # This file
```

## 🎯 Features
- **Web Interface**: Easy-to-use form with 25 input fields
- **API**: RESTful API with automatic validation
- **Predictions**: Premium categories with confidence scores
- **Visualizations**: Interactive charts and risk analysis
- **Model**: Random Forest with preprocessing pipeline

## 📝 Input Fields
**Personal**: Age, Gender, Marital Status, Occupation, Education, Income, Area Type
**Health**: BMI, Smoking, Alcohol, Physical Activity, Sleep, Family History, Medical Conditions
**Insurance**: Policy Type, Tenure, Previous Claims, Premium History

## 🔧 API Usage
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

## 🧠 Model Details
- **Algorithm**: Random Forest Classifier
- **Features**: 25 input features
- **Preprocessing**: StandardScaler + OneHotEncoder + SMOTE
- **Output**: Low/Medium/High premium categories
- **Accuracy**: ~85-90%

## 📋 Requirements
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
streamlit==1.28.0
requests==2.31.0
plotly==5.17.0
pandas==2.1.3
scikit-learn==1.3.2
imbalanced-learn==0.11.0
```

## 🛠 Troubleshooting
- **API not connecting**: Ensure FastAPI is running on port 8000
- **Model not found**: Check `insurance_model.pkl` exists in project root
- **Dependencies**: Run `pip install -r requirements.txt`

## 📞 Support
Create an issue on GitHub for bugs or questions.