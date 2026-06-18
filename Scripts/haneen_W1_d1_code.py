import streamlit as st

st.header('About Me', divider='blue')
st.write("""
I am a student passionate about learning technology and data analysis.
I enjoy exploring Python, Streamlit, and building simple projects to improve my skills.
""")
st.header('Skills', divider='green')
st.markdown("""
- **Python**
- Streamlit
- Data Analysis
- Problem Solving
- Microsoft Excel
""")
st.header('Contact', divider='orange')
st.write("""
📧 Email: haneen@gmail.com

📱 Phone: +91 7908507596

📍 Location: Kerala, India
""")
st.subheader('Favourite Snippet', help='A pattern I use often')
st.code("""
import pandas as pd
df = pd.read_csv("data.csv")
print(df.describe())
""", language="python")
st.markdown("---")
st.latex(r'E = mc^{2}')
st.caption('Built with Streamlit · Day 1 Project · 2024')