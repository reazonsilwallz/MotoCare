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
    st.title("Edit & Delete Records")
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

 # 3 tabs: view records, edit record, delete record
    tab_view, tab_edit, tab_delete = st.tabs([
        "View Records",
        "Edit Record",
        "Delete Record"
    ])

  # View tab: show all records with filters and mini charts
    with tab_view:
        st.subheader(f"All Records — {vehicle_names[active_vid]}")

        if df.empty:
            st.info("No records for this vehicle yet.")
        else:
            # Filters
            fc1, fc2 = st.columns(2)
            cat_filter  = fc1.multiselect(
                "Filter by Category",
                df["category"].unique(),
                key="vf_cat"
            )
            year_filter = fc2.multiselect(
                "Filter by Year",
                sorted(df["date"].dt.year.unique(), reverse=True),
                key="vf_yr"
            )

            filtered = df.copy()
            if cat_filter:
                filtered = filtered[filtered["category"].isin(cat_filter)]
            if year_filter:
                filtered = filtered[filtered["date"].dt.year.isin(year_filter)]

            # Table
            disp = filtered[["date", "category", "description",
                              "cost", "mileage"]].copy()
            disp["date"] = disp["date"].dt.strftime("%d %b %Y")
            disp["cost"] = disp["cost"].map("${:,.2f}".format)
            st.dataframe(disp, use_container_width=True, hide_index=True)
            st.caption(
                f"Showing {len(filtered)} of {len(df)} records  |  "
                f"Total: ${filtered['cost'].sum():,.2f}"
            )

            # Mini charts
            if len(filtered) > 1:
                st.markdown("---")
                vc1, vc2 = st.columns(2)

                with vc1:
                    st.subheader("Category Breakdown")
                    fcat = filtered.groupby("category")["cost"].sum().reset_index()
                    fcat.columns = ["Category", "Cost"]

                    pie = alt.Chart(fcat).mark_arc(innerRadius=40).encode(
                        theta=alt.Theta("Cost:Q"),
                        color=alt.Color("Category:N",
                                        scale=alt.Scale(range=PALETTE),
                                        legend=alt.Legend(orient="bottom")),
                        tooltip=["Category",
                                 alt.Tooltip("Cost:Q", format="$,.2f")]
                    ).properties(height=H_SM).configure_view(
                        strokeWidth=0, fill=CARD_BG
                    ).configure_legend(
                        labelColor=TEXT_CLR, titleColor=TEXT_CLR,
                        fillColor=CARD_BG, strokeColor=GRID_CLR
                    )
                    st.altair_chart(pie, use_container_width=True)

                with vc2:
                    st.subheader("Cost Over Time")
                    ftrend = filtered.sort_values("date").copy()
                    ftrend["Cumulative"] = ftrend["cost"].cumsum()
                    ftrend["date_str"]   = ftrend["date"].dt.strftime("%b %y")

                    line = alt.Chart(ftrend).mark_line(
                        color=ACCENT, strokeWidth=2,
                        point=alt.OverlayMarkDef(color=ACCENT, size=40)
                    ).encode(
                        x=alt.X("date_str:O", axis=alt.Axis(labelAngle=-30)),
                        y=alt.Y("Cumulative:Q", axis=alt.Axis(format="$,.0f")),
                        tooltip=["date_str", "Cumulative", "category"]
                    ).properties(height=H_SM).configure_view(
                        strokeWidth=0, fill=CARD_BG
                    ).configure_axis(
                        gridColor=GRID_CLR, labelColor=TEXT_CLR,
                        titleColor=TEXT_CLR
                    )
                    st.altair_chart(line, use_container_width=True)

            # CSV Export
            st.markdown("---")
            csv_data = filtered.copy()
            csv_data["date"] = csv_data["date"].dt.strftime("%Y-%m-%d")
            v = vehicles[active_vid]
            st.download_button(
                "EXPORT CSV",
                data=csv_data.to_csv(index=False),
                file_name=f"motocare_{v['make']}_{v['model']}.csv",
                mime="text/csv",
            )

# tab 2: edit a record
    with tab_edit:
        st.subheader("Edit a Record")

        if df.empty:
            st.info("No records to edit.")
        else:
            # Dropdown to pick which record to edit
            options = {
                r["id"]: (
                    f"{r['date'].strftime('%d %b %Y')}  —  "
                    f"{r['category']}  —  ${r['cost']:,.2f}"
                )
                for _, r in df.iterrows()
            }

            selected_id = st.selectbox(
                "Select Record to Edit",
                list(options.keys()),
                format_func=lambda x: options[x],
                key="edit_rec_sel",
            )

            # Get the full record dict
            rec = next(
                r for r in st.session_state.data["records"]
                if r["id"] == selected_id
            )

            with st.form("edit_record_form"):
                c1, c2 = st.columns(2)
                new_date = c1.date_input(
                    "Service Date",
                    value=date.fromisoformat(rec["date"])
                )
                new_cat = c2.selectbox(
                    "Category", CATEGORIES,
                    index=CATEGORIES.index(rec["category"])
                )

                new_desc = st.text_area(
                    "Description / Notes",
                    value=rec.get("description", "")
                )

                c3, c4 = st.columns(2)
                new_cost = c3.number_input(
                    "Cost ($)",
                    value=float(rec["cost"]),
                    min_value=0.0,
                    step=0.01,
                    format="%.2f"
                )
                new_mileage = c4.number_input(
                    "Mileage (km)",
                    value=int(rec.get("mileage", 0)),
                    min_value=0,
                    step=1
                )

                update = st.form_submit_button("UPDATE RECORD")

            if update:
                for r in st.session_state.data["records"]:
                    if r["id"] == selected_id:
                        r.update({
                            "date":        str(new_date),
                            "category":    new_cat,
                            "description": new_desc,
                            "cost":        new_cost,
                            "mileage":     new_mileage,
                            "updated_at":  str(datetime.now()),
                        })
                        break
                save_data(st.session_state.data)
                st.success("Record updated!")
                st.rerun()

# tab 3: delete a record
    with tab_delete:
        st.subheader("Delete a Record")

        if df.empty:
            st.info("No records to delete.")
        else:
            options = {
                r["id"]: (
                    f"{r['date'].strftime('%d %b %Y')}  —  "
                    f"{r['category']}  —  ${r['cost']:,.2f}"
                )
                for _, r in df.iterrows()
            }

            del_id = st.selectbox(
                "Select Record to Delete",
                list(options.keys()),
                format_func=lambda x: options[x],
                key="del_rec_sel",
            )

            st.warning(
                f"You are about to permanently delete: "
                f"**{options[del_id]}**"
            )

            if st.button("DELETE RECORD", type="primary"):
                st.session_state.data["records"] = [
                    r for r in st.session_state.data["records"]
                    if r["id"] != del_id
                ]
                save_data(st.session_state.data)
                st.success("Record deleted.")
                st.rerun()

#tab 3: delete a record
    with tab_delete:
        st.subheader("Delete a Record")

        if df.empty:
            st.info("No records to delete.")
        else:
            options = {
                r["id"]: (
                    f"{r['date'].strftime('%d %b %Y')}  —  "
                    f"{r['category']}  —  ${r['cost']:,.2f}"
                )
                for _, r in df.iterrows()
            }

            del_id = st.selectbox(
                "Select Record to Delete",
                list(options.keys()),
                format_func=lambda x: options[x],
                key="delete_rec_sel",
            )

            st.warning(
                f"You are about to permanently delete: "
                f"**{options[del_id]}**"
            )

            if st.button("DELETE RECORD", type="primary", key=f"del_btn_{del_id}"):
                st.session_state.data["records"] = [
                    r for r in st.session_state.data["records"]
                    if r["id"] != del_id
                ]
                save_data(st.session_state.data)
                st.success("Record deleted.")
                st.rerun()