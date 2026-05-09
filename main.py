import streamlit as st
import pandas as pd


# Set page configuration such as title, icon and layout
st.set_page_config(page_title="MotoCare", page_icon="assets/logo.png", layout="wide", initial_sidebar_state="expanded"  )

#title of the app
st.title("MotoCare: Your Ultimate Car Maintenance Companion")
page= st.sidebar.radio("Navigate", ["Home", "Car Selection","Cost","Health","Alerts","Contact Us"])


if page == "Home":
    st.title("Home")

elif page == "Car Selection":
    st.title("Car Selection")

elif page == "Cost":
    st.title("Cost")    

elif page == "Health":
    st.title("Health")

elif page == "Alerts":
    st.title("Alerts")

