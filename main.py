import streamlit as st
import pandas as pd


# Set page configuration such as title, icon and layout
st.set_page_config(page_title="MotoCare", page_icon="assets/logo.png", layout="wide", initial_sidebar_state="expanded"  )

#title of the app
st.title("MotoCare: Your Ultimate Car Maintenance Companion")

# SIDE BAR
st.sidebar.header("MotoCare")
st.sidebar.markdown("Track - Maintain - Drive Safe")
st.sidebar.title("Navigation")

if st.sidebar.button("Dashboard"):
    st.session_state.page = "dashboard"

if st.sidebar.button("Vehicles"):
    st.session_state.page = "vehicles"

if st.sidebar.button("Maintenance"):
    st.session_state.page = "maintenance"

if st.sidebar.button("Costs"):
    st.session_state.page = "costs"

if st.sidebar.button("Settings"):
    st.session_state.page = "settings"

st.subheader(
"Monitor vehicle health, track maintenance, and keep your car running at peak performance."
)





