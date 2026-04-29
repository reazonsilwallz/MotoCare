import streamlit as st
import pandas as pd


st.set_page_config(page_title="MotoCare", page_icon="assets/logo.png", layout="wide")


st.title("MotoCare: Your Ultimate Car Maintenance Companion")

df = pd.read_csv("assets/sample_data.csv")
st.dataframe(df)