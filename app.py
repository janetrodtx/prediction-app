import os  import os
os.environ["OMP_NUM_THREADS"] = "1"  # Fixes signal error for XGBoost

import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Custom CSS for Modern UI
st.markdown("""
    <style>
        /* General Settings */
        body { background-color: #1e1e2f; color: #cfcfcf; font-family: 'Poppins', sans-serif; }
        .sidebar .sidebar-content { background-color: #252633; }
        .stButton > button { background-color: #5c7cfa; border-radius: 8px; }
        .stButton > button:hover { background-color: #4263eb; }
        .stProgress > div > div { background-color: #5c7cfa; }
        .stMetric { background-color: #252633; padding: 10px; border-radius: 8px; }
        .stMetric > div > div > div { color: #fff; }
        .card { background-color: #2e2f3e; padding: 20px; border-radius: 12px; box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2); }
        .stDataFrame { background-color: #2e2f3e; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# Load the trained model
with open("./stroke_risk_model.pkl", "rb") as file:
    model = pickle.load(file)

# Load the scaler for input standardization
with open("./scaler.pkl", "rb") as file:
    scaler = pickle.load(file)

st.title("💖 Stroke Risk Prediction App")
st.markdown("### Simplified and Personalized Stroke Risk Assessment")

# Sidebar for user input
with st.sidebar:
    st.header("Enter Your Details:")
    gender = st.radio("Gender:", ["Male", "Female"])
    age = st.slider("Age:", 0, 100, 25)
    heart_disease = st.radio("Do you have heart disease?", ["Yes", "No"])
    hypertension = st.radio("Do you have hypertension?", ["Yes", "No"])
    previous_stroke = st.radio("Have you had a stroke before?", ["Yes", "No"])
    avg_glucose_level = st.slider("Average Glucose Level:", 0.0, 300.0, 100.0)
    bmi = st.slider("BMI:", 0.0, 60.0, 25.0)
    smoking_status = st.selectbox("Smoking Status:", ["never smoked", "formerly smoked", "smokes"])
    ever_married = st.radio("Have you ever been married?", ["Yes", "No"])
    residence_type = st.radio("Residence Type:", ["Urban", "Rural"])
    work_type = st.selectbox("Work Type:", ["Never_worked", "Private", "Self-employed", "children"])

# Encode user input
def encode_input():
    gender_encoded = 1 if gender == "Male" else 0
    heart_disease_encoded = 1 if heart_disease == "Yes" else 0
    hypertension_encoded = 1 if hypertension == "Yes" else 0
    previous_stroke_encoded = 1 if previous_stroke == "Yes" else 0
    ever_married_encoded = 1 if ever_married == "Yes" else 0
    residence_encoded = 1 if residence_type == "Urban" else 0

    # One-hot encoding for smoking_status
    smoking_status_encoded = [0, 0, 0]
    if smoking_status == "formerly smoked":
        smoking_status_encoded[0] = 1
    elif smoking_status == "never smoked":
        smoking_status_encoded[1] = 1
    elif smoking_status == "smokes":
        smoking_status_encoded[2] = 1

    # One-hot encoding for work_type
    work_type_encoded = [0, 0, 0, 0]
    if work_type == "Never_worked":
        work_type_encoded[0] = 1
    elif work_type == "Private":
        work_type_encoded[1] = 1
    elif work_type == "Self-employed":
        work_type_encoded[2] = 1
    elif work_type == "children":
        work_type_encoded[3] = 1

    # Combine all inputs
    features = [
        gender_encoded, age, hypertension_encoded, heart_disease_encoded,
        previous_stroke_encoded, ever_married_encoded, residence_encoded,
        avg_glucose_level, bmi
    ] + smoking_status_encoded + work_type_encoded

    return np.array(features).reshape(1, -1)

user_input = encode_input()
user_input = scaler.transform(user_input)

risk_score = model.predict_proba(user_input)[0][1]
risk_percentage = risk_score * 100

st.markdown("### 🩺 Your Risk Score:")
st.metric(label="Stroke Risk", value=f"{risk_percentage:.2f}%", delta=None)

st.progress(risk_score)

# Recommendations
st.markdown("### Recommendations:")
if risk_score < 0.3:
    st.success("Low Risk: Maintain a healthy lifestyle.")
elif risk_score < 0.6:
    st.warning("Medium Risk: Consider lifestyle improvements.")
else:
    st.error("High Risk: Consult a healthcare provider immediately.")

st.markdown("---")
st.markdown("📋 **Note:** This prediction is based on the data provided and is not a substitute for professional medical advice.")
