import streamlit as st
import pandas as pd

# Set page configuration such as title, icon and layout
st.set_page_config(page_title="MotoCare", page_icon="assets/logo.png", layout="wide")

#title of the app
st.title("MotoCare: Your Ultimate Car Maintenance Companion")

# SIDE BAR
st.sidebar.header("MotoCare")
st.sidebar.markdown("Track - Maintain - Drive Safe")









# df = pd.read_csv("assets/datasets.csv")
# st.dataframe(df)

# st.subheader("Health Score by Vehicle")
# st.bar_chart(df.set_index("CarName")["HealthScore"])
