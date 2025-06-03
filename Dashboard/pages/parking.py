import streamlit as st
import db

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login to access this page.")
    st.stop()

def get_column_names():
    return ["driver_name", "driver_contact", "vehicle_type", "vehicle_no","exit_time"]

st.title("Parking Management")
role = st.session_state.user["role"]

if role == "admin":
    drivers = db.fetch_all("parking")
    st.dataframe([dict(d) for d in drivers])
    st.subheader("Add Parking Slot")
    with st.form("add_parking_form"):
        driver_name = st.text_input("Driver Name")
        driver_contact = st.text_input("Driver Contact")
        vehicle_type = st.text_input("Vehicle Type")
        vehicle_no = st.text_input("Vehicle No")
        exit_time = st.time_input("Exit Time")
        submitted = st.form_submit_button("Add Parking Slot")
        if submitted:
            db.insert_row(
                "parking",
                ["driver_name", "driver_contact", "vehicle_type", "vehicle_no","exit_time"],
                [driver_name,driver_contact,vehicle_type,vehicle_no,exit_time]
            )
            st.success("Parking Slot Added!")
            st.rerun()

    st.subheader("Edit/Delete Parking")
    drivers_ids = [d["driver_id"] for d in drivers]
    dri_id = st.selectbox("Select Driver Id", drivers_ids)
    selected = next((d for d in drivers if d["driver_id"] == dri_id), None)
    if selected:
        with st.form("edit_parking_form"):
            driver_name = st.text_input("Driver Name", selected["driver_name"])
            driver_contact = st.text_input("Driver Contact", selected["driver_contact"])
            vehicle_type = st.text_input("Vehicle Type", selected["vehicle_type"])
            vehicle_no = st.text_input("Vehicle No", selected["vehicle_no"])
            update_btn = st.form_submit_button("Update Parking")
            delete_btn = st.form_submit_button("Delete Parking")
            if update_btn:
                db.update_row(
                    "parking",
                    ["driver_name", "driver_contact", "vehicle_type", "vehicle_no","exit_time"],
                    [driver_name,driver_contact,vehicle_type,vehicle_no,exit_time],
                    "driver_id",
                    dri_id
                )
                st.success("Parking Updated!")
                st.rerun()
            if delete_btn:
                db.delete_row("parking", "driver_id", dri_id)
                st.success("Parking Slot Deleted!")
                st.rerun()
else:
    st.warning("You do not have permission to view or manage Parking.")
