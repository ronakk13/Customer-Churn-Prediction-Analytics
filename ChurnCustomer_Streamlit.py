import streamlit as st
import pandas as pd
import joblib 

#load model
saved_model = joblib.load(
    "customer_churn_model.pkl"
    )

model = saved_model['model']
features = saved_model['features']

st.title("Customer Churn Prediction")

# =============
# user input 
# =============

gender = st.selectbox("Gender",
                    ["Male","Female"])

seniorcitizen = st.selectbox("SeniorCitizen",
                            ["Yes","No"])

Partner = st.selectbox("Partner",
                    ['Yes','No'])

Dependents = st.selectbox("Dependent",
                        ['Yes','No'])

tenure = st.number_input(
    "Tenure (Months)",
    min_value=0,
    max_value=100,
    value=12
)

monthly_charges = st.number_input(
    "Monthly Charges",
    min_value=0.0,
    max_value=120.0,
    value=70.0
)

total_charges = st.number_input(
    "Total Charges",
    min_value=0.0,
    max_value=8700.0,
    value=1000.0
)

internet = st.selectbox(
    "Internet Service",
    ["DSL","Fiber optic","No"]
)

contract = st.selectbox(
    "Contract",
    ["Month-to-month","One year","Two year"]
)

payment = st.selectbox(
    "Payment Method",
    [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]
)

# Service Columns

multiple_lines = st.selectbox(
    "Multiple Lines",
    ["Yes","No"]
)

online_security = st.selectbox(
    "Online Security",
    ["Yes","No"]
)

online_backup = st.selectbox(
    "Online Backup",
    ["Yes","No"]
)

device_protection = st.selectbox(
    "Device Protection",
    ["Yes","No"]
)

tech_support = st.selectbox(
    "Tech Support",
    ["Yes","No"]
)

streaming_tv = st.selectbox(
    "Streaming TV",
    ["Yes","No"]
)

streaming_movies = st.selectbox(
    "Streaming Movies",
    ["Yes","No"]
)

paperless = st.selectbox(
    "Paperless Billing",
    ["Yes","No"]
)

phone_service = st.selectbox(
    "Phone Service",
    ["Yes","No"]
)

# ======================
# Predict Button
# ======================

if st.button("Predict Churn"):

    # Create Blank DataFrame

    input_df = pd.DataFrame(
        0,
        index=[0],
        columns=features
    )

    # ======================
    # Numerical Features
    # ======================

    input_df["gender"] = 1 if gender=="Male" else 0

    input_df["SeniorCitizen"] = 1 if seniorcitizen=="Yes" else 0 

    input_df["Partner"] = 1 if Partner=="Yes" else 0

    input_df["Dependents"] = 1 if Dependents=="Yes" else 0

    input_df["tenure"] = tenure

    input_df["MonthlyCharges"] = monthly_charges

    input_df["TotalCharges"] = total_charges

    input_df["PhoneService"] = 1 if phone_service=="Yes" else 0

    input_df["PaperlessBilling"] = 1 if paperless=="Yes" else 0


    # ======================
    # Service Features
    # ======================

    service_cols = [
        multiple_lines,
        online_security,
        online_backup,
        device_protection,
        tech_support,
        streaming_tv,
        streaming_movies
    ]

    total_services = sum(
        [1 if x=="Yes" else 0 for x in service_cols]
    )

    input_df["TotalServices"] = total_services

    input_df["MultipleLines"] = 1 if multiple_lines=="Yes" else 0

    input_df["OnlineSecurity"] = 1 if online_security=="Yes" else 0

    input_df["OnlineBackup"] = 1 if online_backup=="Yes" else 0

    input_df["DeviceProtection"] = 1 if device_protection=="Yes" else 0

    input_df["TechSupport"] = 1 if tech_support=="Yes" else 0

    input_df["StreamingTV"] = 1 if streaming_tv=="Yes" else 0

    input_df["StreamingMovies"] = 1 if streaming_movies=="Yes" else 0


    # ======================
    # Risk Score
    # ======================

    risk_score = 0

    if contract == "Month-to-month":
        risk_score += 1

    if payment == "Electronic check":
        risk_score += 1

    if internet == "Fiber optic":
        risk_score += 1

    if seniorcitizen == 1:
        risk_score += 1

    if tenure <= 15:
        risk_score += 1

    input_df["RiskScore"] = risk_score


    # ======================
    # One Hot Columns
    # ======================

    input_df[
        f"InternetService_{internet}"
    ] = 1

    input_df[
        f"Contract_{contract}"
    ] = 1

    input_df[
        f"PaymentMethod_{payment}"
    ] = 1

    # ======================
    # Prediction
    # ======================

    prob = model.predict_proba(
        input_df
    )[0,1]

    prediction = (
        prob >= 0.30
    )

    st.metric(
        "Churn Probability",
        f"{prob*100:.2f}%"
    )

    if prediction:
        st.error(f"⚠️ High Churn Risk ({prob*100:.2f}%)")
    else:
        st.success(f"✅ Low Churn Risk ({prob*100:.2f}%)")