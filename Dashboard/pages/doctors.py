import streamlit as st
import db

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login to access this page.")
    st.stop()
    
def get_column_names():
    # You can hardcode or fetch dynamically for flexibility
    return ["first_name", "last_name", "speciality", "email", "contact_no"]

st.title("Doctors Management")
role = st.session_state.user["role"] if "user" in st.session_state else "user"

doctors = db.fetch_all("doctor LIMIT 2000")
st.dataframe([dict(d) for d in doctors])

if role == "admin":
    st.subheader("Add Doctor")
    with st.form("add_doctor_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        speciality = st.text_input("Speciality")
        email = st.text_input("Email")
        contact_no = st.text_input("Contact No")
        submitted = st.form_submit_button("Add Doctor")
        if submitted:
            db.insert_row(
                "doctor",
                ["first_name", "last_name", "speciality", "email", "contact_no"],
                [first_name, last_name, speciality, email, contact_no]
            )
            st.success("Doctor added!")
            st.rerun()

    st.subheader("Edit/Delete Doctor")
    doctor_ids = [d["doctor_id"] for d in doctors]
    doc_id = st.selectbox("Select Doctor ID", doctor_ids)
    selected = next((d for d in doctors if d["doctor_id"] == doc_id), None)
    if selected:
        with st.form("edit_doctor_form"):
            first_name = st.text_input("First Name", selected["first_name"])
            last_name = st.text_input("Last Name", selected["last_name"])
            speciality = st.text_input("Speciality", selected["speciality"])
            email = st.text_input("Email", selected["email"])
            contact_no = st.text_input("Contact No", selected["contact_no"])
            update_btn = st.form_submit_button("Update Doctor")
            delete_btn = st.form_submit_button("Delete Doctor")
            if update_btn:
                db.update_row(
                    "doctor",
                    ["first_name", "last_name", "speciality", "email", "contact_no"],
                    [first_name, last_name, speciality, email, contact_no],
                    "doctor_id",
                    doc_id
                )
                st.success("Doctor updated!")
                st.rerun()
            if delete_btn:
                db.delete_row("doctor", "doctor_id", doc_id)
                st.success("Doctor deleted!")
                st.rerun()
else:
    st.info("You can only view doctors.")