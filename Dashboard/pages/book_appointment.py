import streamlit as st
import db
from datetime import date

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login to book an appointment.")
    st.stop()

st.title("Book an Appointment")

# Get doctors for dropdown
doctors = db.fetch_query("SELECT doctor_id, first_name, last_name, speciality FROM doctor ORDER BY first_name LIMIT 100")
doctor_options = {f"{d['first_name']} {d['last_name']} ({d['speciality']})": d['doctor_id'] for d in doctors}

with st.form("book_appt"):
    st.subheader("Enter Patient Details")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    doctor = st.selectbox("Select Doctor", list(doctor_options.keys()))
    appt_date = st.date_input("Appointment Date", value=date.today())
    appt_time = st.time_input("Appointment Time")
    reason = st.text_area("Reason for Appointment")
    submit = st.form_submit_button("Request Appointment")
    if submit:
        if not first_name or not last_name:
            st.error("Please enter both first and last name.")
        else:
            db.insert_row(
                "appointment_request",
                ["first_name", "last_name", "doctor_id", "requested_date", "requested_time", "reason"],
                [first_name, last_name, doctor_options[doctor], appt_date, appt_time, reason]
            )
            st.success("Appointment request submitted! You'll be notified when it is approved.")

# Show recent requests (optional, for admin or everyone)
requests = db.fetch_query("SELECT * FROM appointment_request ORDER BY created_at DESC LIMIT 10")
if requests:
    st.subheader("Recent Appointment Requests")
    st.dataframe(requests)