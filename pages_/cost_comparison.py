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
    
# build summary table for all vehicles
    rows = []
    for vid, v in vehicles.items():
        df = records_df(vid)
        rows.append({
            "Vehicle":         f"{v['year']} {v['make']} {v['model']}",
            "Plate":           v.get("plate", "—"),
            "Services":        len(df),
            "Total Cost":      df["cost"].sum()  if not df.empty else 0,
            "Avg per Service": df["cost"].mean() if not df.empty else 0,
            "Highest Bill":    df["cost"].max()  if not df.empty else 0,
            "Last Service":    df["date"].max().strftime("%d %b %Y") if not df.empty else "—",
        })

    summary_df = pd.DataFrame(rows)

    # ── FLEET KPIs ────────────────────────────────────────────────────────────
    fleet_total    = summary_df["Total Cost"].sum()
    fleet_services = int(summary_df["Services"].sum())
    most_expensive = summary_df.loc[
        summary_df["Total Cost"].idxmax(), "Vehicle"
    ] if not summary_df.empty else "—"

    k1, k2, k3 = st.columns(3)
    k1.metric("Fleet Total Spent",     f"${fleet_total:,.2f}")
    k2.metric("Fleet Total Services",   str(fleet_services))
    k3.metric("Most Expensive Vehicle", most_expensive)

    st.markdown("---")