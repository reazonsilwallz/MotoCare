import streamlit as st

def show():
    st.title("ℹ️ About Us")
    st.markdown("---")

    # What is MotoCare?
    st.subheader("🏍️ What is MotoCare?")
    st.write("""
        MotoCare is a personal vehicle maintenance tracking application built
        to help car and motorcycle owners stay on top of their service history
        and costs. Whether you own one vehicle or an entire fleet, MotoCare
        gives you a clear picture of every dollar spent keeping your rides
        on the road.
    """)

    st.markdown("---")

    # some quick stats about the app
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Service Categories", "6")
    k2.metric("App Pages",          "5")
    k3.metric("Vehicles Supported", "Unlimited")
    k4.metric("Cost to Use",        "$0")

    st.markdown("---")

    # Features and navigation
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 Core Features")
        st.write("""
        - Full CRUD for vehicles and records
        - Cost tracking per service and category
        - Cross vehicle cost comparison
        - Interactive charts and analytics
        - CSV export for your records
        - 100% offline — data stored locally
        """)

    with col2:
        st.subheader("🗺️ How to Navigate")
        st.write("""
        - **Dashboard** — KPIs and charts for any vehicle
        - **Select a Vehicle** — register vehicles and add records
        - **Cost Comparison** — compare spend across all vehicles
        - **Edit & Delete Records** — update or remove any record
        - **About Us** — you are here!
        """)

    st.markdown("---")