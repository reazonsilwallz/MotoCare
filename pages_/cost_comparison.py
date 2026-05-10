import streamlit as st
import altair as alt
import pandas as pd
from helpers import get_vehicles, get_records, records_df

# Chart styling constants
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


def show():
    st.title("📊 Cost Comparison")
    st.markdown("---")

    vehicles = get_vehicles()

    if not vehicles:
        st.warning("No vehicles found. Go to **Select a Vehicle** to add one.")
        return