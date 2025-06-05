import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px

# Configuration
API_URL = "http://localhost:8000/predict"
HEALTH_URL = "http://localhost:8000/health"

# Page configuration
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2e8b57;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .result-box {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🏥 Insurance Premium Category Predictor</h1>', unsafe_allow_html=True)
st.markdown("### Enter your personal and health details to predict your insurance premium category")

# Check API health
try:
    health_response = requests.get(HEALTH_URL, timeout=5)
    if health_response.status_code == 200:
        health_data = health_response.json()
        if health_data.get("model_status") == "healthy":
            st.success("✅ API is connected and model is ready!")
        else:
            st.warning("⚠️ API is connected but model may not be loaded properly.")
    else:
        st.error("❌ API health check failed.")
except:
    st.error("❌ Cannot connect to API. Make sure FastAPI server is running on port 8000.")

# Sidebar for navigation and info
with st.sidebar:
    st.markdown("### 📋 Instructions")
    st.markdown("""
    1. Fill in all the required fields
    2. Click 'Predict Premium Category'
    3. View your prediction results
    4. Check the probability breakdown
    """)
    
    st.markdown("### ℹ️ About")
    st.markdown("""
    This app predicts insurance premium categories:
    - **Low**: Lower premium rates
    - **Medium**: Standard premium rates  
    - **High**: Higher premium rates
    """)

# Create two columns for better layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-header">👤 Personal Information</div>', unsafe_allow_html=True)
    
    # Personal Information
    personal_col1, personal_col2 = st.columns(2)
    
    with personal_col1:
        age = st.number_input("Age", min_value=1, max_value=119, value=30, help="Your current age")
        gender = st.selectbox("Gender", options=["Male", "Female", "Other"], help="Select your gender")
        marital_status = st.selectbox("Marital Status", 
                                    options=["Single", "Married", "Divorced", "Widowed"],
                                    help="Your current marital status")
        education = st.selectbox("Education Level",
                                options=["None", "Primary", "SSC", "HSC", "Bachelor", "Master", "PhD"],
                                help="Your highest education level")
    
    with personal_col2:
        occupation = st.selectbox("Occupation",
                                options=["Private Job", "Farmer", "Freelancer", "Teacher", 
                                       "Student", "Doctor", "Unemployed", "Construction Worker"],
                                help="Your current occupation")
        monthly_income = st.number_input("Monthly Income", min_value=1.0, value=50000.0, 
                                       help="Your monthly income in your local currency")
        area_type = st.selectbox("Area Type", 
                               options=["Urban", "Rural", "Semi-urban"],
                               help="Type of area where you live")
        loyalty_score = st.slider("Loyalty Score", min_value=0.0, max_value=1.0, value=0.5, step=0.01,
                                help="Your loyalty score with the insurance company")

    st.markdown('<div class="section-header">🏥 Health Information</div>', unsafe_allow_html=True)
    
    # Health Information
    health_col1, health_col2 = st.columns(2)
    
    with health_col1:
        bmi = st.number_input("BMI (Body Mass Index)", min_value=10.0, max_value=50.0, value=25.0,
                            help="Your Body Mass Index (weight/height²)")
        smoking_status = st.selectbox("Smoking Status", 
                                    options=["Never", "Former", "Current"],
                                    help="Your smoking habits")
        alcohol_consumption = st.selectbox("Alcohol Consumption",
                                         options=["Never", "Occasional", "Regular"],
                                         help="Your alcohol consumption frequency")
        physical_activity = st.number_input("Physical Activity (hours/week)", 
                                          min_value=0.0, max_value=50.0, value=5.0,
                                          help="Hours of physical activity per week")
    
    with health_col2:
        sleep_hours = st.number_input("Sleep Hours per Day", 
                                    min_value=1.0, max_value=24.0, value=7.0,
                                    help="Average hours of sleep per day")
        family_history = st.selectbox("Family History of Medical Conditions",
                                    options=["Yes", "No"],
                                    help="Family history of medical conditions")
        preexisting_condition = st.selectbox("Preexisting Medical Condition",
                                           options=["None", "Asthma", "Diabetes", "Hypertension", "Heart Disease"],
                                           help="Any preexisting medical conditions")
        doctor_visits = st.number_input("Doctor Visits Last Year", 
                                      min_value=1, max_value=50, value=2,
                                      help="Number of doctor visits in the last year")

    st.markdown('<div class="section-header">💊 Medications & Lifestyle</div>', unsafe_allow_html=True)
    
    # Medications & Lifestyle
    lifestyle_col1, lifestyle_col2 = st.columns(2)
    
    with lifestyle_col1:
        current_medications = st.selectbox("Currently on Medications",
                                         options=["No", "Yes"],
                                         help="Are you currently taking any medications?")
        stress_level = st.selectbox("Stress Level",
                                  options=["Low", "Moderate", "High"],
                                  help="Your general stress level")
        pollution_exposure = st.selectbox("Pollution Exposure Level",
                                        options=["Low", "Moderate", "High"],
                                        help="Your exposure to environmental pollution")
    
    with lifestyle_col2:
        food_habit = st.selectbox("Food Habits",
                                options=["Home-cooked", "Mixed", "Mostly Restaurant"],
                                help="Your primary food consumption habits")
        claim_history = st.number_input("Previous Claims Count", 
                                      min_value=0, max_value=20, value=0,
                                      help="Number of previous insurance claims")
        claim_amount_last_year = st.number_input("Claim Amount Last Year", 
                                               min_value=0.0, value=0.0,
                                               help="Total claim amount in the last year")

    st.markdown('<div class="section-header">🏦 Insurance Information</div>', unsafe_allow_html=True)
    
    # Insurance Information
    insurance_col1, insurance_col2 = st.columns(2)
    
    with insurance_col1:
        insurance_type = st.selectbox("Insurance Type",
                                    options=["Basic", "Comprehensive", "Family", "Critical Illness"],
                                    help="Type of insurance coverage you want")
        policy_tenure = st.number_input("Policy Tenure (years)", 
                                      min_value=1, max_value=10, value=5,
                                      help="Duration of the insurance policy in months")
    
    with insurance_col2:
        premium_paid_last_year = st.number_input("Premium Paid Last Year", 
                                               min_value=0.0, value=0.0,
                                               help="Premium amount paid in the last year")

with col2:
    st.markdown('<div class="section-header">🎯 Prediction Results</div>', unsafe_allow_html=True)
    
    # Prediction button
    if st.button("🔮 Predict Premium Category", type="primary", use_container_width=True):
        # Prepare input data
        input_data = {
            "Age": age,
            "Gender": gender,
            "Marital_Status": marital_status,
            "Occupation": occupation,
            "Education": education,
            "Monthly_Income": monthly_income,
            "Area_Type": area_type,
            "BMI": bmi,
            "Smoking_Status": smoking_status,
            "Alcohol_Consumption": alcohol_consumption,
            "Physical_Activity_hr_wk": physical_activity,
            "Sleep_hr_day": sleep_hours,
            "Family_History": family_history,
            "Preexisting_Condition": preexisting_condition,
            "Doctor_Visits_Last_Year": doctor_visits,
            "Current_Medications": current_medications,
            "Stress_Level": stress_level,
            "Pollution_Exposure": pollution_exposure,
            "Food_Habit": food_habit,
            "Claim_History": claim_history,
            "Claim_Amount_Last_Year": claim_amount_last_year,
            "Insurance_Type": insurance_type,
            "Policy_Tenure": policy_tenure,
            "Premium_Paid_Last_Year": premium_paid_last_year,
            "Loyalty_Score": loyalty_score
        }
        
        try:
            # Make API request
            with st.spinner("🔄 Processing your data..."):
                response = requests.post(API_URL, json=input_data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                predicted_category = result.get('premium_category', 'Unknown')
                confidence = result.get('confidence', 0)
                probabilities = result.get('probabilities', {})
                
                # Display main result
                if predicted_category == "Low":
                    st.markdown(f'''
                    <div class="result-box success-box">
                        <h3>✅ Predicted Category: {predicted_category}</h3>
                        <p><strong>Confidence:</strong> {confidence:.2%}</p>
                        <p>Great news! You qualify for lower premium rates.</p>
                    </div>
                    ''', unsafe_allow_html=True)
                elif predicted_category == "Medium":
                    st.markdown(f'''
                    <div class="result-box warning-box">
                        <h3>⚡ Predicted Category: {predicted_category}</h3>
                        <p><strong>Confidence:</strong> {confidence:.2%}</p>
                        <p>You qualify for standard premium rates.</p>
                    </div>
                    ''', unsafe_allow_html=True)
                else:  # High
                    st.markdown(f'''
                    <div class="result-box error-box">
                        <h3>⚠️ Predicted Category: {predicted_category}</h3>
                        <p><strong>Confidence:</strong> {confidence:.2%}</p>
                        <p>Higher premium rates may apply due to risk factors.</p>
                    </div>
                    ''', unsafe_allow_html=True)
                
                # Display probability breakdown
                st.markdown("### 📊 Probability Breakdown")
                
                # Create a DataFrame for the chart
                prob_df = pd.DataFrame(list(probabilities.items()), columns=['Category', 'Probability'])
                prob_df['Probability_Percent'] = prob_df['Probability'] * 100
                
                # Create bar chart
                fig = px.bar(prob_df, x='Category', y='Probability_Percent',
                           title='Premium Category Probabilities',
                           color='Category',
                           color_discrete_map={'Low': '#28a745', 'Medium': '#ffc107', 'High': '#dc3545'})
                fig.update_layout(
                    showlegend=False, 
                    height=300,
                    yaxis_title='Probability (%)',
                    xaxis_title='Premium Category'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Display detailed probabilities
                for category, probability in probabilities.items():
                    st.write(f"**{category}:** {probability:.2%}")
                
                # Risk factors analysis
                st.markdown("### 🔍 Risk Factor Analysis")
                risk_factors = []
                
                if smoking_status == "Current":
                    risk_factors.append("Current smoker")
                if alcohol_consumption == "Regular":
                    risk_factors.append("Regular alcohol consumption")
                if stress_level == "High":
                    risk_factors.append("High stress level")
                if pollution_exposure == "High":
                    risk_factors.append("High pollution exposure")
                if preexisting_condition != "None":
                    risk_factors.append(f"Preexisting condition: {preexisting_condition}")
                if bmi > 30:
                    risk_factors.append("BMI indicates obesity")
                if physical_activity < 2:
                    risk_factors.append("Low physical activity")
                
                if risk_factors:
                    st.markdown("**Identified Risk Factors:**")
                    for factor in risk_factors:
                        st.write(f"• {factor}")
                else:
                    st.success("✅ No major risk factors identified!")
                
            else:
                error_detail = response.json().get('detail', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
                st.error(f"❌ API Error: {response.status_code}\n\n{error_detail}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the FastAPI server. Make sure it's running on port 8000.")
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. The server might be overloaded.")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🏥 Insurance Premium Category Predictor | Built with Streamlit & FastAPI</p>
    <p><small>Disclaimer: This is a predictive tool and should not be considered as final insurance advice.</small></p>
</div>
""", unsafe_allow_html=True)

# Debug section (expandable)
with st.expander("🛠️ Debug Information"):
    st.markdown("### API Endpoints")
    st.code(f"Prediction API: {API_URL}")
    st.code(f"Health Check API: {HEALTH_URL}")
    
    st.markdown("### Sample Input Format")
    sample_input = {
        "Age": 30,
        "Gender": "Male",
        "Marital_Status": "Single",
        "Occupation": "Private Job",
        "Education": "Bachelor",
        "Monthly_Income": 50000,
        "Area_Type": "Urban",
        "BMI": 25.0,
        "Smoking_Status": "Never",
        "Alcohol_Consumption": "Never",
        "Physical_Activity_hr_wk": 5.0,
        "Sleep_hr_day": 7.0,
        "Family_History": "No",
        "Preexisting_Condition": "None",
        "Doctor_Visits_Last_Year": 2,
        "Current_Medications": "No",
        "Stress_Level": "Low",
        "Pollution_Exposure": "Low",
        "Food_Habit": "Home-cooked",
        "Claim_History": 0,
        "Claim_Amount_Last_Year": 0,
        "Insurance_Type": "Basic",
        "Policy_Tenure": 5,
        "Premium_Paid_Last_Year": 0,
        "Loyalty_Score": 0.5
    }
    st.json(sample_input)