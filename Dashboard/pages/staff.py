import streamlit as st
import db

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login to access this page.")
    st.stop()

def get_column_names():
    return ["first_name", "last_name", "staff_role","contact_number"]

st.title("Staff Management")
role = st.session_state.user["role"]

if role == "admin":
    staffs = db.fetch_all("staff")
    st.dataframe([dict(s) for s in staffs])
    st.subheader("Add Staff Member")
    with st.form("add_staff_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        staff_role = st.text_input("Role")
        contact_number = st.text_input("Contact No")
        submitted = st.form_submit_button("Add Staff Member")
        if submitted:
            db.insert_row(
                "staff",
                ["first_name", "last_name", "staff_role","contact_number"],
                [first_name, last_name, staff_role,contact_number]
            )
            st.success("Staff Member Added!")
            st.rerun()

    st.subheader("Edit/Delete Saff Member")
    staffs_ids = [s["staff_id"] for s in staffs]
    sta_id = st.selectbox("Select Staff Id", staffs_ids)
    selected = next((s for s in staffs if s["staff_id"] == sta_id), None)
    if selected:
        with st.form("edit_staff_form"):
            first_name = st.text_input("First Name", selected["first_name"])
            last_name    = st.text_input("Lasr Name", selected["last_name"])
            staff_role = st.text_input("Member Role", selected["staff_role"])
            contact_number = st.text_input("Contact No", selected["contact_number"])

            update_btn = st.form_submit_button("Update Staff Member")
            delete_btn = st.form_submit_button("Delete Staff Member")
            if update_btn:
                db.update_row(
                    "parking",
                    ["first_name", "last_name", "staff_role","contact_number"],
                    [first_name, last_name, staff_role,contact_number],
                    "staff_id",
                    sta_id
                )
                st.success("Member Updated!")
                st.rerun()
            if delete_btn:
                db.delete_row("staff", "staff_id", sta_id)
                st.success("Member Deleted!")
                st.rerun()
else:
    st.warning("You do not have permission to view or manage Staff.")
