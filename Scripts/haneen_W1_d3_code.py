import streamlit as st
import pandas as pd

st.title("🏋️ BMI & Daily Calorie Calculator")
st.markdown("Calculate your BMI, daily calorie needs, and ideal weight range.")
st.markdown("---")

st.header("Personal Details")
name = st.text_input("Name")
age = st.number_input(
    "Age",
    min_value=10,
    max_value=100,
    value=20
)

sex = st.radio(
    "Sex",
    ["Male", "Female"],
    horizontal=True
)
weight = st.slider(
    "Weight (kg)",
    min_value=30,
    max_value=150,
    value=70
)
height = st.slider(
    "Height (cm)",
    min_value=100,
    max_value=220,
    value=170
)
st.write(
    f"Name: {name} | Age: {age} | Sex: {sex} | Weight: {weight} kg | Height: {height} cm"
)
st.header("BMI Calculator")

height_m = height / 100
bmi = round(weight / (height_m ** 2), 1)

if bmi < 18.5:
    category = "Underweight"
    risk = "Moderate"
    status_message = "Underweight - Moderate Risk"
    status_type = "warning"

elif bmi < 25:
    category = "Normal weight"
    risk = "Low"
    status_message = "Normal Weight - Low Risk"
    status_type = "success"

elif bmi < 30:
    category = "Overweight"
    risk = "Elevated"
    status_message = "Overweight - Elevated Risk"
    status_type = "warning"

else:
    category = "Obese"
    risk = "High"
    status_message = "Obese - High Risk"
    status_type = "error"

st.metric("BMI", bmi)

if status_type == "success":
    st.success(status_message)
elif status_type == "warning":
    st.warning(status_message)
else:
    st.error(status_message)

st.header("Daily Calorie Need")

activity = st.selectbox(
    "Select Activity Level",
    [
        "Sedentary",
        "Lightly Active",
        "Moderately Active",
        "Very Active"
    ]
)

if sex == "Male":
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
else:
    bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

activity_multiplier = {
    "Sedentary": 1.2,
    "Lightly Active": 1.375,
    "Moderately Active": 1.55,
    "Very Active": 1.725
}

daily_calories = round(
    bmr * activity_multiplier[activity]
)

st.metric(
    "Daily Calorie Requirement",
    f"{daily_calories} kcal"
)

st.header("Ideal Weight Range")

height_inches = height / 2.54

if sex == "Male":
    ideal_weight = 52 + (1.9 * (height_inches - 60))
else:
    ideal_weight = 49 + (1.7 * (height_inches - 60))

low_weight = round(ideal_weight * 0.9, 1)
high_weight = round(ideal_weight * 1.1, 1)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Minimum Ideal Weight",
        f"{low_weight} kg"
    )
with col2:
    st.metric(
        "Maximum Ideal Weight",
        f"{high_weight} kg"
    )

st.header("Full Summary")

if st.button("Show My Summary"):
    st.subheader("Summary Report")
    st.write(f"👤 Name: {name}")
    st.write(f"🎂 Age: {age}")
    st.write(f"⚧ Sex: {sex}")
    st.write(f"⚖️ Weight: {weight} kg")
    st.write(f"📏 Height: {height} cm")
    st.write(f"📊 BMI: {bmi}")
    st.write(f"🏷️ Classification: {category}")
    st.write(f"❤️ Health Risk: {risk}")
    st.write(f"🔥 Daily Calories Needed: {daily_calories} kcal")
    st.write(
        f"🎯 Ideal Weight Range: {low_weight} kg - {high_weight} kg"
    )
    