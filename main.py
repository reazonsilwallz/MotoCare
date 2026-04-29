import streamlit as st
import pandas as pd

# Set page configuration such as title, icon and layout
st.set_page_config(page_title="MotoCare", page_icon="assets/logo.png", layout="wide")

#title of the app
st.title("MotoCare: Your Ultimate Car Maintenance Companion")

# SIDE BAR
st.sidebar.header("MotoCare")
st.sidebar.markdown("Track - Maintain - Drive Safe")

page=st.sidebar.radio(
    "Navigation",
    ("Home", "Maintenance Schedule", "Health Score", "Service History", "Tips & Resources")
)

st.write(
"Monitor vehicle health, track maintenance, and keep your car running at peak performance."
)


# App Description
st.subheader("Features")

st.write("1. Track vehicle health")
st.write("2. Log maintenance history")
st.write("3. Service reminders")
st.write("4. View analytics")







# df = pd.read_csv("assets/datasets.csv")
# st.dataframe(df)

# st.subheader("Health Score by Vehicle")
# st.bar_chart(df.set_index("CarName")["HealthScore"])
