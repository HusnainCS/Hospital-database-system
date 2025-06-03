import streamlit as st
import db

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login to access this page.")
    st.stop()

st.title("Laboratory Management")
role = st.session_state.user["role"]
laboratorys = db.fetch_all("laboratory LIMIT 7000")

if laboratorys:
    st.dataframe([dict(l) for l in laboratorys])
else:
    st.info("No Laboratory Tests found.")

# --- For Admin: View, Update, Delete Tests ---
if role == "admin" and laboratorys:
    st.subheader("Update or Delete Laboratory Test")
    lab_ids = [l["test_id"] for l in laboratorys]
    selected_id = st.selectbox("Select Laboratory Test ID", lab_ids)
    selected = next((l for l in laboratorys if l["test_id"] == selected_id), None)

    # Fetch patients and doctors for editing
    patients = db.fetch_all("patient")
    doctors = db.fetch_all("doctor")
    patient_options = {f"{p['first_name']} {p['last_name']} (ID: {p['patient_id']})": p["patient_id"] for p in patients}
    doctor_options = {f"{d['first_name']} {d['last_name']} ({d['speciality']})": d["doctor_id"] for d in doctors}

    if selected:
        # Safe index for patient
        patient_values = list(patient_options.values())
        doctor_values = list(doctor_options.values())
        try:
            patient_index = patient_values.index(selected["patient_id"])
        except ValueError:
            patient_index = 0  # fallback if not found

        try:
            doctor_index = doctor_values.index(selected["doctor_id"])
        except ValueError:
            doctor_index = 0  # fallback if not found

        with st.form("edit_test_form"):
            patient = st.selectbox(
                "Patient",
                list(patient_options.keys()),
                index=patient_index
            )
            doctor = st.selectbox(
                "Doctor",
                list(doctor_options.keys()),
                index=doctor_index
            )
            test_name = st.text_input("Test Name", selected["test_name"])
            test_date = st.date_input("Test Date", selected["test_date"])
            test_time = st.time_input("Test Time", selected["test_time"])
            test_result = st.text_input("Test Results", selected["test_result"])

            update_btn = st.form_submit_button("Update Laboratory Test")
            delete_btn = st.form_submit_button("Delete Laboratory Test")

            if update_btn:
                db.update_row(
                    "laboratory",
                    ["patient_id", "doctor_id", "test_name", "test_date", "test_time", "test_result"],
                    [
                        patient_options[patient],
                        doctor_options[doctor],
                        test_name,
                        test_date,
                        test_time,
                        test_result
                    ],
                    "test_id",
                    selected_id
                )
                st.success("Test updated!")
                st.rerun()
            if delete_btn:
                db.delete_row("laboratory", "test_id", selected_id)
                st.success("Test deleted!")
                st.rerun()
elif role != "admin":
    st.warning("You can only view the Laboratory Tests")