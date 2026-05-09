import streamlit as st
import pandas as pd
import json
import os
from datetime import date, datetime
import uuid
import altair as alt

# Constants
DATA_FILE = 'motocare_data.json'

CATEGORIES =[
    'Oil Change', 'Tire Services', 'Brake Services', 'Battery Services', 'Engine Tune-Up', 'Others',
]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"vehicles": {}, "services": {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def init_state():
    if 'data' not in st.session_state:
        st.session_state.data = load_data()

init_state()

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
        return pd.DataFrame(columns=["id", "vehicle_id", "date", "category",
                                     "description", "cost", "mileage"])
    df = pd.DataFrame(recs)
    df["date"] = pd.to_datetime(df["date"])
    df["cost"] = df["cost"].astype(float)
    return df.sort_values("date", ascending=False)

## test code
if __name__ == "__main__":
    data = load_data()
    print(data)  

    data["vehicles"]["test-id"] = {"make": "Toyota", "model": "Camry"}
    save_data(data)

    reloaded = load_data()
    print(reloaded)  