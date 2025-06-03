import streamlit as st
import db

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login to access this page.")
    st.stop()

def get_column_names():
    return ["receptionist_name", "contact_no"]

st.title("Reception Management")
role = st.session_state.user["role"]

if role == "admin":
    receptions = db.fetch_all("reception")
    st.dataframe([dict(r) for r in receptions])
    st.subheader("Add Receptionist Member")
    with st.form("add_receptionist_form"):
        receptionist_name = st.text_input("Receptionist Name")
        contact_no = st.text_input("Contact No")

        submitted = st.form_submit_button("Add Receptionist")
        if submitted:
            db.insert_row(
                "reception",
                ["receptionist_name", "contact_no"],
                [receptionist_name, contact_no]
            )
            st.success("Receptionist Added!")
            st.rerun()

    st.subheader("Edit/Delete Receptionist")
    receptionist_id = [r["receptionist_id"] for r in receptions]
    rec_id = st.selectbox("Select Receptionist Id", receptionist_id)
    selected = next((r for r in receptions if r["receptionist_id"] == rec_id), None)
    if selected:
        with st.form("edit_receptionist_form"):
            receptionist_name = st.text_input("Receptionist Name", selected["receptionist_name"])
            contact_no = st.text_input("Contact No", selected["contact_no"])

            update_btn = st.form_submit_button("Update Receptionist")
            delete_btn = st.form_submit_button("Delete Receptionist")
            if update_btn:
                db.update_row(
                    "reception",
                   ["receptionist_name", "contact_no"],
                   [receptionist_name, contact_no],
                     "receptionist_id",
                    rec_id
                )
                st.success("Receptionist Updated!")
                st.rerun()
            if delete_btn:
                db.delete_row("reception", "receptionist_id", rec_id)
                st.success("Receptionist Deleted!")
                st.rerun()
else:
    st.warning("You do not have permission to view or manage Reception.")
