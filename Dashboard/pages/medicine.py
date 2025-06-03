import streamlit as st
import db

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login to access this page.")
    st.stop()
    
def get_column_names():
    # You can hardcode or fetch dynamically for flexibility
    return ["medicine_name", "dosage", "purpose","manufacturer" ]

st.title("Medicine Management")
role = st.session_state.user["role"] if "user" in st.session_state else "user"

medicines = db.fetch_all("medicine LIMIT 3000")
st.dataframe([dict(m) for m in medicines])

if role == "admin":
    st.subheader("Add Medicine")
    with st.form("add_medicine_form"):
        medicine_name = st.text_input("Medicine Name")
        dosage = st.text_input("Dosage")
        purpose = st.text_input("Purpose")
        manufacturer = st.text_input("Manufacturer")
        submitted = st.form_submit_button("Add Medicine")
        if submitted:
            db.insert_row(
                "medicine",
                ["medicine_name", "dosage", "purpose", "manufacturer"],
                [medicine_name, dosage, purpose, manufacturer]
            )
            st.success("Medicine added!")
            st.rerun()

    st.subheader("Edit/Delete Medicine")
    medicine_ids = [m["medicine_id"] for m in medicines]
    med_id = st.selectbox("Select Medicine ID", medicine_ids)
    selected = next((m for m in medicines if m["medicine_id"] == med_id), None)
    if selected:
        with st.form("edit_medicine_form"):
            medicine_name = st.text_input("Medicine Name", selected["medicine_name"])
            dosage = st.text_input("Dosage", selected["dosage"])
            purpose = st.text_input("Purpose", selected["purpose"])
            manufacturer = st.text_input("Manufacturer", selected["manufacturer"])

            update_btn = st.form_submit_button("Update Medicine")
            delete_btn = st.form_submit_button("Delete Medicine")
            if update_btn:
                db.update_row(
                    "medicine",
                    ["medicine_name", "dosage", "purpose", "manufacturer"],
                    [medicine_name, dosage, purpose, manufacturer],
                    "medicine_id",
                    med_id
                )
                st.success("Medicine updated!")
                st.rerun()
            if delete_btn:
                db.delete_row("medicine", "medicine_id", med_id)
                st.success("Medicine deleted!")
                st.rerun()
else:
    st.info("You can only view Medicines.")