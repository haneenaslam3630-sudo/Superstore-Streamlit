import streamlit as st  
import pandas as pd

st.title("📊 Student Performance Dashboard")

data={
    "Name":
    ["Aisha","Bob","Clera","Dev","Eva","Finn","Grace","Hiro","Ines","Jai",],
    "Math":[88,52,76,91,43,67,85,59,78,95],
    "Science":[72,45,88,83,38,71,90,62,55,88],
    "English":[65,70,82,77,60,58,74,88,91,73],
    "Art":[90,85,60,55,78,92,68,75,83,61],
}
df=pd.DataFrame(data)
df["Average"]=df[["Math","Science","English","Art"]].mean(axis=1).round(1)


st.dataframe(df, hide_index=True, use_container_width=True)


st.write(f"Total number of students: {len(df)}")

class_avg = df["Average"].mean()
highest_avg = df["Average"].max()
lowest_avg = df["Average"].min()
students_above_70 = (df["Average"] >= 70).sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Class Average", f"{class_avg:.1f}")

with col2:
    st.metric("Highest Average", f"{highest_avg:.1f}")

with col3:
    st.metric("Lowest Average", f"{lowest_avg:.1f}")

with col4:
    st.metric("Students ≥ 70", students_above_70)


def highlight_average(value):
    if value >= 70:
        return "color: green"
    else:
        return "color: red"


styled_df = df.style.map(
    highlight_average,
    subset=["Average"]
)


st.dataframe(
    styled_df,
    hide_index=True,
    use_container_width=True
)


top3 = df.sort_values(by="Average", ascending=False).head(3).reset_index(drop=True)

top3.insert(0, "Rank", range(1, len(top3) + 1))

st.subheader("🏆 Top 3 Students")
st.table(top3)


subject_summary = {
    "Math": {
        "Minimum Score": df["Math"].min(),
        "Maximum Score": df["Math"].max(),
        "Class Mean": round(df["Math"].mean(), 1)
    },
    "Science": {
        "Minimum Score": df["Science"].min(),
        "Maximum Score": df["Science"].max(),
        "Class Mean": round(df["Science"].mean(), 1)
    },
    "English": {
        "Minimum Score": df["English"].min(),
        "Maximum Score": df["English"].max(),
        "Class Mean": round(df["English"].mean(), 1)
    },
    "Art": {
        "Minimum Score": df["Art"].min(),
        "Maximum Score": df["Art"].max(),
        "Class Mean": round(df["Art"].mean(), 1)
    }
}


st.subheader("📚 Subject Summary")
st.json(subject_summary)

from datetime import date


st.divider()


st.caption(
    f"Created by Haneen Aslam | Student Performance Dashboard | {date.today()}"
)