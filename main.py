import streamlit as st
import pandas as pd
import json
import os
from datetime import date, datetime
import uuid
import altair as alt
from PIL import Image

# Constants
DATA_FILE = 'motocare_data.json' # local storage file

CATEGORIES =[
    'Oil Change', 'Tire Services', 'Brake Services', 'Battery Services', 'Engine Tune-Up', 'Others',
]

# Data FUnctions
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"vehicles": {}, "records": []}

def save_data(data):
    # overwrite the entire file with updated data
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def init_state():
    # Load data into session state once — persists across reruns
    if 'data' not in st.session_state:
        st.session_state.data = load_data()

init_state()

# Helper functions
def get_vehicles():
    return st.session_state.data["vehicles"]


def get_records(vehicle_id=None):
    recs = st.session_state.data["records"]
    if vehicle_id:
        recs = [r for r in recs if r["vehicle_id"] == vehicle_id]
    return recs


def records_df(vehicle_id=None):
    recs = get_records(vehicle_id)
    if not recs:
        # Return empty DataFrame with correct columns if no records
        return pd.DataFrame(columns=["id", "vehicle_id", "date", "category",
                                     "description", "cost", "mileage"])
    df = pd.DataFrame(recs)
    df["date"] = pd.to_datetime(df["date"])
    df["cost"] = df["cost"].astype(float)
    return df.sort_values("date", ascending=False)


icon = Image.open("assets/logo.png")

# Page Configuration
st.set_page_config(
    page_title="MotoCare - Motorcycle Maintenance Tracker",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
)


# Sidebar Navigation
st.sidebar.image("assets/logo.png", use_container_width=True)
st.sidebar.title("MotoCare")
st.sidebar.markdown("Drive -- Maintain -- Thrive")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Select a Vehicle",
        "Cost Comparison",
        "Edit & Delete Records",
        "About Us",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.caption("v1.0.0 · MIT License")

# Chart theme and colors
CARD_BG  = "#111111"
GRID_CLR = "#1e1e1e"
TEXT_CLR = "#888888"
ACCENT   = "#e63a00"
ACCENT2  = "#ff9966"
ACCENT3  = "#ffcc00"
ACCENT4  = "#4ecdc4"
ACCENT5  = "#a29bfe"
PALETTE  = [ACCENT, ACCENT2, ACCENT3, ACCENT4, ACCENT5,
            "#fd79a8", "#55efc4", "#74b9ff", "#ffeaa7", "#b2bec3"]

H_SM  = 220
H_MED = 280
H_LG  = 320

# Read vehicles once — used by every page
vehicles = get_vehicles()
vehicle_names = {
    vid: f"{v['year']} {v['make']} {v['model']}"
    for vid, v in vehicles.items()
}

# Page Routes
from pages import dashboard, select_vehicle, cost_comparison, edit_delete, about

if page == "Dashboard":
    dashboard.show()

elif page == "Select a Vehicle":
    select_vehicle.show()

elif page == "Cost Comparison":
    cost_comparison.show()

elif page == "Edit & Delete Records":
    edit_delete.show()

elif page == "About Us":
    about.show()



