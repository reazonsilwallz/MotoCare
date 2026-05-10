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

#Row 1 - Total Cost Bar + Cost Share Pie
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Total Cost per Vehicle")

        bar = alt.Chart(summary_df).mark_bar(
            color=ACCENT,
            cornerRadiusTopRight=3,
            cornerRadiusBottomRight=3
        ).encode(
            x=alt.X("Total Cost:Q", axis=alt.Axis(format="$,.0f")),
            y=alt.Y("Vehicle:N",    sort="-x"),
            tooltip=["Vehicle", alt.Tooltip("Total Cost:Q", format="$,.2f")]
        ).properties(height=H_MED).configure_view(
            strokeWidth=0, fill=CARD_BG
        ).configure_axis(
            gridColor=GRID_CLR, labelColor=TEXT_CLR, titleColor=TEXT_CLR
        )
        st.altair_chart(bar, use_container_width=True)

    with col2:
        st.subheader("Fleet Cost Share")

        pie = alt.Chart(summary_df).mark_arc(innerRadius=50).encode(
            theta=alt.Theta("Total Cost:Q"),
            color=alt.Color("Vehicle:N",
                            scale=alt.Scale(range=PALETTE),
                            legend=alt.Legend(orient="bottom")),
            tooltip=["Vehicle", alt.Tooltip("Total Cost:Q", format="$,.2f")]
        ).properties(height=H_MED).configure_view(
            strokeWidth=0, fill=CARD_BG
        ).configure_legend(
            labelColor=TEXT_CLR, titleColor=TEXT_CLR,
            fillColor=CARD_BG, strokeColor=GRID_CLR
        )
        st.altair_chart(pie, use_container_width=True)

    # Row 2 - Avg Cost per Service + Number of Services
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Average Cost per Service")

        avg_bar = alt.Chart(summary_df).mark_bar(
            color=ACCENT2,
            cornerRadiusTopRight=3,
            cornerRadiusBottomRight=3
        ).encode(
            x=alt.X("Avg per Service:Q", axis=alt.Axis(format="$,.0f")),
            y=alt.Y("Vehicle:N", sort="-x"),
            tooltip=["Vehicle", alt.Tooltip("Avg per Service:Q", format="$,.2f")]
        ).properties(height=H_SM).configure_view(
            strokeWidth=0, fill=CARD_BG
        ).configure_axis(
            gridColor=GRID_CLR, labelColor=TEXT_CLR, titleColor=TEXT_CLR
        )
        st.altair_chart(avg_bar, use_container_width=True)

    with col4:
        st.subheader("Number of Services")

        svc_bar = alt.Chart(summary_df).mark_bar(
            color=ACCENT3,
            cornerRadiusTopLeft=3,
            cornerRadiusTopRight=3
        ).encode(
            x=alt.X("Vehicle:O",  axis=alt.Axis(labelAngle=-15)),
            y=alt.Y("Services:Q"),
            tooltip=["Vehicle", "Services"]
        ).properties(height=H_SM).configure_view(
            strokeWidth=0, fill=CARD_BG
        ).configure_axis(
            gridColor=GRID_CLR, labelColor=TEXT_CLR, titleColor=TEXT_CLR
        )
        st.altair_chart(svc_bar, use_container_width=True)

    st.markdown("---")

   #Monthly Spend by Vehicle Line Chart
    st.subheader("Monthly Spend by Vehicle")

    all_records = get_records()

    if all_records:
        all_df = pd.DataFrame(all_records)
        all_df["date"]    = pd.to_datetime(all_df["date"])
        all_df["cost"]    = all_df["cost"].astype(float)
        all_df["Month"]   = all_df["date"].dt.to_period("M").astype(str)
        all_df["Vehicle"] = all_df["vehicle_id"].map(
            lambda x: f"{vehicles[x]['year']} {vehicles[x]['make']} {vehicles[x]['model']}"
            if x in vehicles else "Unknown"
        )

        mon_veh = all_df.groupby(["Month", "Vehicle"])["cost"].sum().reset_index()
        mon_veh.columns = ["Month", "Vehicle", "Cost"]

        line = alt.Chart(mon_veh).mark_line(
            strokeWidth=2, point=True
        ).encode(
            x=alt.X("Month:O",   axis=alt.Axis(labelAngle=-30)),
            y=alt.Y("Cost:Q",    axis=alt.Axis(format="$,.0f")),
            color=alt.Color("Vehicle:N",
                            scale=alt.Scale(range=PALETTE),
                            legend=alt.Legend(orient="bottom")),
            tooltip=["Month", "Vehicle", alt.Tooltip("Cost:Q", format="$,.2f")]
        ).properties(height=H_LG).configure_view(
            strokeWidth=0, fill=CARD_BG
        ).configure_axis(
            gridColor=GRID_CLR, labelColor=TEXT_CLR, titleColor=TEXT_CLR
        ).configure_legend(
            labelColor=TEXT_CLR, titleColor=TEXT_CLR,
            fillColor=CARD_BG, strokeColor=GRID_CLR
        )
        st.altair_chart(line, use_container_width=True)

    st.markdown("---")

    # Category Breakdown per Vehicle
    st.subheader("Category Breakdown per Vehicle")

    if all_records:
        cat_veh = all_df.groupby(["category", "Vehicle"])["cost"].sum().reset_index()
        cat_veh.columns = ["Category", "Vehicle", "Cost"]

        cat_bar = alt.Chart(cat_veh).mark_bar(
            cornerRadiusTopLeft=2,
            cornerRadiusTopRight=2
        ).encode(
            x=alt.X("Category:O",  axis=alt.Axis(labelAngle=-20)),
            y=alt.Y("Cost:Q",      axis=alt.Axis(format="$,.0f")),
            color=alt.Color("Vehicle:N",
                            scale=alt.Scale(range=PALETTE),
                            legend=alt.Legend(orient="bottom")),
            xOffset="Vehicle:N",
            tooltip=["Category", "Vehicle", alt.Tooltip("Cost:Q", format="$,.2f")]
        ).properties(height=H_LG).configure_view(
            strokeWidth=0, fill=CARD_BG
        ).configure_axis(
            gridColor=GRID_CLR, labelColor=TEXT_CLR,
            titleColor=TEXT_CLR, labelAngle=-20
        ).configure_legend(
            labelColor=TEXT_CLR, titleColor=TEXT_CLR,
            fillColor=CARD_BG, strokeColor=GRID_CLR
        )
        st.altair_chart(cat_bar, use_container_width=True)

    st.markdown("---")

    # Full Comparison Table
    st.subheader("Full Comparison Table")

    fmt_df = summary_df.set_index("Vehicle").copy()
    fmt_df["Total Cost"]      = fmt_df["Total Cost"].map("${:,.2f}".format)
    fmt_df["Avg per Service"] = fmt_df["Avg per Service"].map("${:,.2f}".format)
    fmt_df["Highest Bill"]    = fmt_df["Highest Bill"].map("${:,.2f}".format)
    st.dataframe(fmt_df, use_container_width=True)