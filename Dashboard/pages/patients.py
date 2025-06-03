import streamlit as st
import db

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login to access this page.")
    st.stop()
    
def get_column_names():
    # You can hardcode or fetch dynamically for flexibility
    return ["first_name", "last_name", "age", "date_of_birth", "gender", "contact_no", "email", "address"]

st.title("Patients Management")
role = st.session_state.user["role"]

if role == "admin":
    patients = db.fetch_all("patient LIMIT 5000")
    st.dataframe([dict(p) for p in patients])

    st.subheader("Add Patient")
    with st.form("add_patient_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        age = st.text_input("Age")
        date_of_birth = st.date_input("Date of Birth")
        gender = st.text_input("Gender")
        contact_no = st.text_input("Contact No")
        email = st.text_input("Email")
        address = st.text_input("Address")

        submitted = st.form_submit_button("Add Patient")
        if submitted:
            db.insert_row(
                "patient",
                ["first_name", "last_name", "age","date_of_birth","gender","contact_no","email","address"],
                [first_name, last_name, age, date_of_birth, gender, contact_no, email, address]
            )
            st.success("Patient added!")
            st.rerun()

    st.subheader("Edit/Delete Patient")
    patients_ids = [p["patient_id"] for p in patients]
    pt_id = st.selectbox("Select Patient ID", patients_ids)
    selected = next((p for p in patients if p["patient_id"] == pt_id), None)
    if selected:
        with st.form("edit_doctor_form"):
            first_name = st.text_input("First Name", selected["first_name"])
            last_name = st.text_input("Last Name", selected["last_name"])
            age = st.text_input("Age", selected["age"])
            date_of_birth = st.date_input("Date of Birth", selected["date_of_birth"])
            gender = st.text_input("Gender", selected["gender"])
            contact_number = st.text_input("Contact No", selected["contact_number"])
            email = st.text_input("Email", selected["email"])
            address = st.text_input("Address", selected["address"])

            update_btn = st.form_submit_button("Update Patient")
            delete_btn = st.form_submit_button("Delete Patient")
            if update_btn:
                db.update_row(
                    "patient",
                    ["first_name", "last_name", "age","date_of_birth","gender", "contact_number","email","address"],
                    [first_name, last_name, age,date_of_birth, gender, contact_number, email, address],
                    "patient_id",
                    pt_id
                )
                st.success("Patient updated!")
                st.rerun()
            if delete_btn:
                db.delete_row("patient", "patient_id", pt_id)
                st.success("Patient deleted!")
                st.rerun()
else:
    st.warning("You do not have permission to view or manage patients.")