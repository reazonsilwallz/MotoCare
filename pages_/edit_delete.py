import streamlit as st
import altair as alt
import pandas as pd
from datetime import date, datetime
from helpers import get_vehicles, get_records, records_df, save_data, CATEGORIES

#Chart styling constants
CARD_BG  = "#111111"
GRID_CLR = "#1e1e1e"
TEXT_CLR = "#888888"
ACCENT   = "#e63a00"
ACCENT2  = "#ff9966"
PALETTE  = [ACCENT, ACCENT2, "#ffcc00", "#4ecdc4", "#a29bfe",
            "#fd79a8", "#55efc4", "#74b9ff", "#ffeaa7", "#b2bec3"]

H_SM = 220


def show():
    st.title("✏️ Edit & Delete Records")
    st.markdown("---")

    vehicles = get_vehicles()

    if not vehicles:
        st.warning("No vehicles found. Go to **Select a Vehicle** to add one.")
        return

    # Vehicle selector
    vehicle_names = {
        vid: f"{v['year']} {v['make']} {v['model']}"
        for vid, v in vehicles.items()
    }

    active_vid = st.selectbox(
        "Select Vehicle",
        list(vehicle_names.keys()),
        format_func=lambda x: vehicle_names[x],
        key="edr_vid",
    )

    df = records_df(active_vid)
    st.markdown("---")