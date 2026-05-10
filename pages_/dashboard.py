import streamlit as st
import altair as alt
import pandas as pd
from helpers import get_vehicles, get_records, records_df

# chart styling constants
CARD_BG  = "#ffffff"
GRID_CLR = "#e0e0e0"
TEXT_CLR = "#444444"
ACCENT   = "#1a3a6b"   # Navy blue — primary
ACCENT2  = "#2e6fbd"   # Medium blue
ACCENT3  = "#f0a500"   # Gold
ACCENT4  = "#e63a00"   # Red
ACCENT5  = "#4ecdc4"   # Teal
PALETTE  = [ACCENT, ACCENT2, ACCENT3, ACCENT4, ACCENT5,
            "#6c5ce7", "#00b894", "#fd79a8", "#fdcb6e", "#74b9ff"]

H_SM  = 220
H_MED = 280


def show():
    st.title("Dashboard")
    st.markdown("---")

    vehicles = get_vehicles()

    if not vehicles:
        st.warning("No vehicles found. Go to **Select a Vehicle** to add one.")
        return

    # vehicle selector
    vehicle_names = {
        vid: f"{v['year']} {v['make']} {v['model']}"
        for vid, v in vehicles.items()
    }

    active_vid = st.selectbox(
        "Select Vehicle",
        list(vehicle_names.keys()),
        format_func=lambda x: vehicle_names[x],
        key="dash_vid",
    )

    v  = vehicles[active_vid]
    df = records_df(active_vid)

    st.markdown(f"### {v['year']} {v['make']} {v['model']}  —  `{v.get('plate','—')}`")
    st.markdown("---")

    # kpi cards
    total_cost      = df["cost"].sum()  if not df.empty else 0
    num_services    = len(df)
    last_service    = df["date"].max().strftime("%d %b %Y") if not df.empty else "—"
    avg_cost        = df["cost"].mean() if not df.empty else 0
    current_mileage = int(df["mileage"].max()) if not df.empty else int(v.get("mileage", 0))

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Spent",     f"${total_cost:,.2f}")
    c2.metric("Services",         str(num_services))
    c3.metric("Last Service",     last_service)
    c4.metric("Avg Cost",        f"${avg_cost:,.2f}")
    c5.metric("Current Mileage", f"{current_mileage:,} km")

    st.markdown("---")

    if df.empty:
        st.info("No records yet. Add records via **Select a Vehicle**.")
        return

    # row 1 - cumulative cost + category breakdown
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Cumulative Cost Over Time")

        trend = df.sort_values("date").copy()
        trend["Cumulative Cost"] = trend["cost"].cumsum()
        trend["date_str"] = trend["date"].dt.strftime("%b %Y")

        line = alt.Chart(trend).mark_line(
            color=ACCENT, strokeWidth=2,
            point=alt.OverlayMarkDef(color=ACCENT, size=40)
        ).encode(
            x=alt.X("date_str:O", axis=alt.Axis(labelAngle=-30, labelColor=TEXT_CLR,
                                                  domainColor=GRID_CLR, tickColor=GRID_CLR)),
            y=alt.Y("Cumulative Cost:Q", axis=alt.Axis(format="$,.0f",
                                                        labelColor=TEXT_CLR,
                                                        domainColor=GRID_CLR,
                                                        tickColor=GRID_CLR)),
            tooltip=["date_str", "Cumulative Cost", "category"]
        ).properties(height=H_MED)

        area = alt.Chart(trend).mark_area(
            color=ACCENT, opacity=0.1
        ).encode(
            x="date_str:O",
            y="Cumulative Cost:Q",
        )

        chart = (area + line).configure_view(
            strokeWidth=0, fill=CARD_BG
        ).configure_axis(
            gridColor=GRID_CLR, labelColor=TEXT_CLR, titleColor=TEXT_CLR
        )
        st.altair_chart(chart, use_container_width=True)

    with col2:
        st.subheader("Spend by Category")

        cat_df = df.groupby("category")["cost"].sum().reset_index()
        cat_df.columns = ["Category", "Cost"]

        pie = alt.Chart(cat_df).mark_arc(innerRadius=50).encode(
            theta=alt.Theta("Cost:Q"),
            color=alt.Color("Category:N",
                            scale=alt.Scale(range=PALETTE),
                            legend=alt.Legend(orient="bottom",
                                              labelColor=TEXT_CLR,
                                              titleColor=TEXT_CLR)),
            tooltip=["Category", alt.Tooltip("Cost:Q", format="$,.2f")]
        ).properties(height=H_MED).configure_view(
            strokeWidth=0, fill=CARD_BG
        ).configure_legend(
            labelColor=TEXT_CLR, titleColor=TEXT_CLR,
            fillColor=CARD_BG, strokeColor=GRID_CLR
        )
        st.altair_chart(pie, use_container_width=True)

    # recent service table
    st.markdown("---")
    st.subheader("Recent Services")

    disp = df.head(6)[["date", "category", "description", "cost", "mileage"]].copy()
    disp["date"] = disp["date"].dt.strftime("%d %b %Y")
    disp["cost"] = disp["cost"].map("${:,.2f}".format)
    st.dataframe(disp, use_container_width=True, hide_index=True)

    st.markdown("---")
    
    # row 2 - Monthly Bar + Cost per Service Dot
    col3, = st.columns(1)

    with col3:
        st.subheader("Monthly Spend")

        monthly = df.copy()
        monthly["Month"] = monthly["date"].dt.to_period("M").astype(str)
        mon_df = monthly.groupby("Month")["cost"].sum().reset_index()
        mon_df.columns = ["Month", "Cost"]

        bar = alt.Chart(mon_df).mark_bar(
            color=ACCENT2,
            cornerRadiusTopLeft=3,
            cornerRadiusTopRight=3
        ).encode(
            x=alt.X("Month:O", axis=alt.Axis(labelAngle=-30)),
            y=alt.Y("Cost:Q", axis=alt.Axis(format="$,.0f")),
            tooltip=["Month", alt.Tooltip("Cost:Q", format="$,.2f")]
        ).properties(height=H_SM).configure_view(
            strokeWidth=0, fill=CARD_BG
        ).configure_axis(
            gridColor=GRID_CLR, labelColor=TEXT_CLR, titleColor=TEXT_CLR
        )
        st.altair_chart(bar, use_container_width=True)


