import streamlit as st
import pandas as pd


st.set_page_config(page_title="MotoCare", page_icon="assets/logo.png", layout="wide")


st.title("MotoCare: Your Ultimate Car Maintenance Companion")

df = pd.read_csv("assets/datasets.csv")
st.dataframe(df)

st.subheader("Health Score by Vehicle")
st.bar_chart(df.set_index("CarName")["HealthScore"])