import streamlit as st
import db

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login to access this page.")
    st.stop()

st.title("Prescription Management")
role = st.session_state.user["role"]
prescriptions = db.fetch_all("prescription LIMIT 10000")

if prescriptions:
    st.dataframe([dict(p) for p in prescriptions])
else:
    st.info("No Prescription found.")

# --- For Admin: View, Update, Delete Tests ---
if role == "admin" and prescriptions:
    st.subheader("Update or Delete Prescription Test")
    prc_ids = [p["prescription_id"] for p in prescriptions]
    selected_id = st.selectbox("Select Prescription ID", prc_ids)
    selected = next((p for p in prescriptions if p["prescription_id"] == selected_id), None)

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

        with st.form("edit_prescription_form"):
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
            patient_procedure = st.text_input("Procedure", selected["patient_procedure"])
            procedure_date = st.date_input("Procedure Date", selected["procedure_date"])
            next_appointment = st.text_input("Next Appointment ", selected["next_appointment"])

            update_btn = st.form_submit_button("Update Prescription")
            delete_btn = st.form_submit_button("Delete Prescription")

            if update_btn:
                db.update_row(
                    "prescription",
                    ["patient_id", "doctor_id", "patient_procedure", "procedure_date", "next_appointment"],
                    [
                        patient_options[patient],
                        doctor_options[doctor],
                        patient_procedure,
                        procedure_date,
                        next_appointment,
                    ],
                    "prescription_id",
                    selected_id
                )
                st.success("Prescription updated!")
                st.rerun()
            if delete_btn:
                db.delete_row("prescription", "prescription_id", selected_id)
                st.success("Prescription deleted!")
                st.rerun()
elif role != "admin":
    st.warning("You can only view the Prescription")