import streamlit as st
import pandas as pd
from src.pipelines.predict_pipeline import Predictor

data = pd.read_csv("artifacts/raw_data.csv", header=0)

print("📁 File Loaded Successfully!")
print("📁 Data:", data)
print("📝 Columns in Data:", list(data.columns))
print("🔍 First 5 Rows:\n", data.head())

st.title("Used Car Price Predictor")
st.dataframe(data)
st.dataframe(data.head())
st.subheader(data.columns)

form = st.form("car_details_form")

# Categorical features
car_name = form.selectbox("Enter the Car Name", data["car_name"].unique())
seller_type = form.selectbox("Enter the Seller Type", data["seller_type"].unique())
fuel_type = form.selectbox("Enter the Fuel Type", data["fuel_type"].unique())
transmission_type = form.selectbox("Enter the Transmission Type", data["transmission_type"].unique())

# Numerical features
vehicle_age = form.number_input("Enter Vehicle Age", step=1, min_value=0)
km_driven = form.number_input("Enter KMs Driven", step=1, min_value=0)
mileage = form.number_input("Enter Mileage", step=1, min_value=0)
engine = form.number_input("Enter Engine Capacity", step=1, min_value=0)
max_power = form.number_input("Enter Max Power", step=1, min_value=0)
seats = form.number_input("Enter Number of Seats", step=1, min_value=0)

submitted = form.form_submit_button("Predict")

if submitted:
    y_pred = Predictor().predict(
        car_name=car_name,
        seller_type=seller_type,
        fuel_type=fuel_type,
        transmission_type=transmission_type,
        vehicle_age=vehicle_age,
        km_driven=km_driven,
        mileage=mileage,
        engine=engine,
        max_power=max_power,
        seats=seats
    )
    
    st.text(f"Rupees {y_pred}")

