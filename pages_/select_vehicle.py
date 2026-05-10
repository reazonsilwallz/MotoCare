import streamlit as st
from datetime import date, datetime
import uuid

# Import from helpers — NOT from main
from helpers import (
    get_vehicles,
    get_records,
    save_data,
    CATEGORIES,
)

def show():
    st.title("Select a Vehicle")
    st.markdown("---")

    tab_add_v, tab_all_v, tab_add_rec = st.tabs([
        "Add Vehicle",
        "All Vehicles",
        "Add Maintenance Record"
    ])

    with tab_add_v:
        st.subheader("Add a New Vehicle")

        with st.form("add_vehicle_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            year  = c1.number_input("Year",
                                     min_value=1900,
                                     max_value=date.today().year + 1,
                                     value=date.today().year,
                                     step=1)
            make  = c2.text_input("Make",  placeholder="e.g. Honda")
            model = c3.text_input("Model", placeholder="e.g. Civic")

            c4, c5, c6 = st.columns(3)
            plate   = c4.text_input("License Plate", placeholder="e.g. ABC-1234")
            vin     = c5.text_input("VIN (optional)")
            mileage = c6.number_input("Current Mileage (km)", min_value=0, step=1)

            color  = st.text_input("Color (optional)", placeholder="e.g. Matte Black")
            save_v = st.form_submit_button("ADD VEHICLE")

        if save_v:
            if not make or not model:
                st.error("Make and Model are required.")
            else:
                vid = str(uuid.uuid4())
                st.session_state.data["vehicles"][vid] = {
                    "year":       int(year),
                    "make":       make,
                    "model":      model,
                    "plate":      plate,
                    "vin":        vin,
                    "mileage":    mileage,
                    "color":      color,
                    "created_at": str(datetime.now()),
                }
                save_data(st.session_state.data)
                st.success(f"{year} {make} {model} registered!")
                st.rerun()

    with tab_all_v:
        st.subheader("Your Registered Vehicles")

        vehicles = get_vehicles()

        if not vehicles:
            st.info("No vehicles registered yet.")
        else:
            for vid, v in vehicles.items():
                recs  = get_records(vid)
                total = sum(float(r["cost"]) for r in recs)

                with st.expander(
                    f"{v['year']} {v['make']} {v['model']}  —  {v.get('plate','—')}"
                ):
                    cc1, cc2, cc3, cc4 = st.columns(4)
                    cc1.metric("Services",    len(recs))
                    cc2.metric("Total Spent", f"${total:,.2f}")
                    cc3.metric("Mileage",     f"{int(v.get('mileage',0)):,} km")
                    cc4.metric("Color",       v.get("color","—") or "—")

                    if v.get("vin"):
                        st.caption(f"VIN: {v['vin']}")

                    st.markdown("---")

                    with st.form(f"edit_v_{vid}"):
                        st.markdown("**Edit vehicle details**")

                        ec1, ec2, ec3 = st.columns(3)
                        ny   = ec1.number_input("Year",
                                                 min_value=1900,
                                                 max_value=date.today().year + 1,
                                                 value=int(v["year"]),
                                                 step=1, key=f"ey_{vid}")
                        nm   = ec2.text_input("Make",  value=v["make"],
                                               key=f"em_{vid}")
                        nmod = ec3.text_input("Model", value=v["model"],
                                               key=f"emod_{vid}")

                        ec4, ec5, ec6 = st.columns(3)
                        nplate = ec4.text_input("Plate",
                                                 value=v.get("plate",""),
                                                 key=f"ep_{vid}")
                        nvin   = ec5.text_input("VIN",
                                                 value=v.get("vin",""),
                                                 key=f"ev_{vid}")
                        nmi    = ec6.number_input("Mileage",
                                                   min_value=0,
                                                   value=int(v.get("mileage",0)),
                                                   step=1, key=f"emi_{vid}")
                        ncolor = st.text_input("Color",
                                               value=v.get("color",""),
                                               key=f"ec_{vid}")
                        upd_v  = st.form_submit_button("UPDATE VEHICLE")

                    if upd_v:
                        st.session_state.data["vehicles"][vid].update({
                            "year":       int(ny),
                            "make":       nm,
                            "model":      nmod,
                            "plate":      nplate,
                            "vin":        nvin,
                            "mileage":    nmi,
                            "color":      ncolor,
                            "updated_at": str(datetime.now()),
                        })
                        save_data(st.session_state.data)
                        st.success("✅ Vehicle updated!")
                        st.rerun()

                    st.markdown("---")

                    confirm_del = st.checkbox(
                        f"Delete {v['year']} {v['make']} {v['model']} and all its records",
                        key=f"del_chk_{vid}"
                    )
                    if st.button("DELETE VEHICLE",
                                 key=f"del_v_{vid}",
                                 disabled=not confirm_del):
                        del st.session_state.data["vehicles"][vid]
                        st.session_state.data["records"] = [
                            r for r in st.session_state.data["records"]
                            if r["vehicle_id"] != vid
                        ]
                        save_data(st.session_state.data)
                        st.success("🗑️ Vehicle deleted.")
                        st.rerun()

    with tab_add_rec:
        st.subheader("Add a Maintenance Record")

        vehicles = get_vehicles()

        if not vehicles:
            st.warning("Register a vehicle first.")
        else:
            vehicle_names_local = {
                vid: f"{v['year']} {v['make']} {v['model']}"
                for vid, v in vehicles.items()
            }
            rec_vid = st.selectbox(
                "Select Vehicle",
                list(vehicle_names_local.keys()),
                format_func=lambda x: vehicle_names_local[x],
                key="rec_vid_sel",
            )

            with st.form("add_record_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                service_date = c1.date_input("Service Date", value=date.today())
                category     = c2.selectbox("Category", CATEGORIES)

                description = st.text_area(
                    "Description / Notes",
                    placeholder="e.g. Changed oil filter and 5W-30 full synthetic"
                )

                c3, c4 = st.columns(2)
                cost    = c3.number_input("Cost ($)",
                                           min_value=0.0,
                                           step=0.01,
                                           format="%.2f")
                mileage = c4.number_input("Mileage at Service (km)",
                                           min_value=0, step=1)

                submitted = st.form_submit_button("SAVE RECORD")

            if submitted:
                record = {
                    "id":          str(uuid.uuid4()),
                    "vehicle_id":  rec_vid,
                    "date":        str(service_date),
                    "category":    category,
                    "description": description,
                    "cost":        cost,
                    "mileage":     mileage,
                    "created_at":  str(datetime.now()),
                }
                st.session_state.data["records"].append(record)
                save_data(st.session_state.data)
                st.success("✅ Maintenance record saved!")