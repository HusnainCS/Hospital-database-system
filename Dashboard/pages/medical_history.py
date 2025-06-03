import streamlit as st
import db

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login to access this page.")
    st.stop()

st.title("Medical History Management")
role = st.session_state.user["role"]
medical_historys = db.fetch_all("medical_history LIMIT 10000")

if medical_historys:
    st.dataframe([dict(m) for m in medical_historys])
else:
    st.info("No Medical History found.")

# --- For Admin: View, Update, Delete Tests ---
if role == "admin" and medical_historys:
    st.subheader("Update or Delete Medical History")
    med_ids = [m["record_id"] for m in medical_historys]
    selected_id = st.selectbox("Select Record ID", med_ids)
    selected = next((m for m in medical_historys if m["record_id"] == selected_id), None)

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
            diagnosis = st.text_input("Diagnosis", selected["diagnosis"])
            treatment_plan = st.date_input("Treatment Plan", selected["treatment_plan"])
            admission_date = st.text_input("Admission Date ", selected["admission_date"])
            discharge_date = st.text_input("Discharge Date ", selected["discharge_date"])

            update_btn = st.form_submit_button("Update Record")
            delete_btn = st.form_submit_button("Delete Record")

            if update_btn:
                db.update_row(
                    "medical_history",
                    ["patient_id", "doctor_id", "diagnosis", "treatment_plan", "admission_date", "discharge_date"],
                    [
                        patient_options[patient],
                        doctor_options[doctor],
                        diagnosis,
                        treatment_plan,
                        admission_date,
                        discharge_date,
                    ],
                    "record_id",
                    selected_id
                )
                st.success("Record updated!")
                st.rerun()
            if delete_btn:
                db.delete_row("medical_history", "record_id", selected_id)
                st.success("Record deleted!")
                st.rerun()
elif role != "admin":
    st.warning("You can only view the Medical History")