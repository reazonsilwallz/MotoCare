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