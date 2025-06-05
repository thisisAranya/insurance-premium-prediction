from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, Annotated, Union
import pickle
import pandas as pd
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Insurance Premium Prediction API",
    description="API for predicting insurance premium categories based on user data",
    version="1.0.0"
)

# Load the trained pipeline
try:
    with open('insurance_model.pkl', 'rb') as f:
        pipeline = pickle.load(f)
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    print("❌ Model file 'insurance_model.pkl' not found!")
    pipeline = None
except Exception as e:
    print(f"❌ Error loading model: {e}")
    pipeline = None

# Input schema based on your training data
class UserInput(BaseModel):
    Age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the user")]
    Gender: Literal["Male", "Female", "Other"] = Field(..., description="Gender of the user")
    Marital_Status: Literal["Single", "Married", "Divorced", "Widowed"] = Field(..., description="Marital status")
    Occupation: Literal[
        "Private Job", "Farmer", "Freelancer", "Teacher", "Student", "Doctor", "Unemployed", "Construction Worker"
    ] = Field(..., description="Occupation of the user")
    Education: Literal["HSC", "Bachelor", "Master", "None", "PhD", "Primary", "SSC"] = Field(..., description="Education level")
    Monthly_Income: Annotated[float, Field(..., gt=0, description="Monthly income")]
    Area_Type: Literal["Urban", "Rural", "Semi-urban"] = Field(..., description="Residential area type")
    BMI: Annotated[float, Field(..., gt=0, description="Body Mass Index")]
    Smoking_Status: Literal["Never", "Former", "Current"] = Field(..., description="Smoking status")
    Alcohol_Consumption: Literal["Never", "Occasional", "Regular"] = Field(..., description="Alcohol consumption")
    Physical_Activity_hr_wk: Annotated[float, Field(..., gt=0, description="Physical activity per week (hours)")]
    Sleep_hr_day: Annotated[float, Field(..., gt=0, description="Sleep per day (hours)")]
    Family_History: Literal["Yes", "No"] = Field(..., description="Family history of conditions")
    Preexisting_Condition: Literal['None', 'Asthma', 'Diabetes', 'Hypertension', 'Heart Disease'] = Field(..., description="Preexisting conditions")
    Doctor_Visits_Last_Year: Annotated[int, Field(..., gt=0, description="Doctor visits last year")]
    
    # Current_Medications can accept both string and int for flexibility
    Current_Medications: Union[Literal["Yes", "No"], Literal[0, 1]] = Field(..., description="Currently on medications (Yes/No or 1/0)")
    
    Stress_Level: Literal["Low", "Moderate", "High"] = Field(..., description="Stress level")
    Pollution_Exposure: Literal["Low", "Moderate", "High"] = Field(..., description="Pollution exposure")
    Food_Habit: Literal["Home-cooked", "Mostly Restaurant", "Mixed"] = Field(..., description="Food habit")
    Claim_History: Annotated[int, Field(..., ge=0, description="Previous claim history")]
    Claim_Amount_Last_Year: Annotated[float, Field(..., ge=0, description="Claim amount in last year")]
    Insurance_Type: Literal["Comprehensive", "Basic", "Family", "Critical Illness"] = Field(..., description="Insurance type")
    Policy_Tenure: Annotated[int, Field(..., gt=0, le=10, description="Policy tenure (months)")]
    Premium_Paid_Last_Year: Annotated[float, Field(..., ge=0, description="Premium paid last year")]
    Loyalty_Score: Annotated[float, Field(..., gt=0, le=1, description="Loyalty score")]

# Field name mapping from API input to training data column names
field_mapping = {
    'Age': 'age',
    'Gender': 'gender',
    'Marital_Status': 'marital_status',
    'Occupation': 'occupation',
    'Education': 'education',
    'Monthly_Income': 'monthly_income',
    'Area_Type': 'area_type',
    'BMI': 'bmi',
    'Smoking_Status': 'smoking_status',
    'Alcohol_Consumption': 'alcohol_consumption',
    'Physical_Activity_hr_wk': 'physical_activity_hr_wk',
    'Sleep_hr_day': 'sleep_hr_day',
    'Family_History': 'family_history',
    'Preexisting_Condition': 'preexisting_condition',
    'Doctor_Visits_Last_Year': 'doctor_visits_last_year',
    'Current_Medications': 'current_medications',
    'Stress_Level': 'stress_level',
    'Pollution_Exposure': 'pollution_exposure',
    'Food_Habit': 'food_habit',
    'Claim_History': 'claim_history',
    'Claim_Amount_Last_Year': 'claim_amount_last_year',
    'Insurance_Type': 'insurance_type',
    'Policy_Tenure': 'policy_tenure',
    'Premium_Paid_Last_Year': 'premium_paid_last_year',
    'Loyalty_Score': 'loyalty_score'
}

def convert_medications_to_numeric(value):
    """Convert Current_Medications to numeric format (0/1)"""
    if isinstance(value, str):
        return 1 if value.lower() == "yes" else 0
    return value  # Already numeric

@app.post("/predict")
def predict_premium(user_input: UserInput):
    """Predict insurance premium category"""
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not available. Please check if the model file exists.")
    
    try:
        # Convert input to dict
        input_data_raw = user_input.dict()
        
        # Convert Current_Medications to numeric if needed
        input_data_raw['Current_Medications'] = convert_medications_to_numeric(input_data_raw['Current_Medications'])
        
        # Map field names to expected column names (matching training data after lowercase conversion)
        input_data = {field_mapping[k]: v for k, v in input_data_raw.items()}
        
        # Create DataFrame with the same structure as training data
        input_df = pd.DataFrame([input_data])
        
        # Use the pipeline to predict (it handles preprocessing automatically)
        prediction = pipeline.predict(input_df)
        
        # Get prediction probabilities
        prediction_proba = pipeline.predict_proba(input_df)
        
        # Get class labels
        classes = pipeline.named_steps['classifier'].classes_
        
        # Create probability dictionary
        probabilities = {str(cls): float(prob) for cls, prob in zip(classes, prediction_proba[0])}
        
        return {
            "premium_category": str(prediction[0]),
            "probabilities": probabilities,
            "confidence": float(max(prediction_proba[0])),
            "input_processed": input_data
        }
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Input validation error: {ve}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    model_status = "healthy" if pipeline is not None else "model_not_loaded"
    return {
        "status": "healthy",
        "model_status": model_status,
        "message": "API is running smoothly" if pipeline is not None else "API running but model not loaded"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )