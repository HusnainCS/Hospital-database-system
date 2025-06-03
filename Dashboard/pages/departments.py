import streamlit as st
import db

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login to access this page.")
    st.stop()

def get_column_names():
    return ["department_name", "department_location"]

st.title("Department Management")
role = st.session_state.user["role"]

departments = db.fetch_all("department")
st.dataframe([dict(d) for d in departments])

if role == "admin":
    st.subheader("Add Department")
    with st.form("add_department_form"):
        department_name = st.text_input("Department Name")
        department_location = st.text_input("Department Location")
        submitted = st.form_submit_button("Add Department")
        if submitted:
            db.insert_row(
                "department",
                ["department_name", "department_location"],
                [department_name, department_location]
            )
            st.success("Department Added!")
            st.rerun()

    st.subheader("Edit/Delete Department")
    departments_ids = [d["department_id"] for d in departments]
    dep_id = st.selectbox("Select Department Id", departments_ids)
    selected = next((d for d in departments if d["department_id"] == dep_id), None)
    if selected:
        with st.form("edit_department_form"):
            department_name = st.text_input("Department Name", selected["department_name"])
            department_location = st.text_input("Department Location", selected["department_location"])
            update_btn = st.form_submit_button("Update Department")
            delete_btn = st.form_submit_button("Delete Department")
            if update_btn:
                db.update_row(
                    "department",
                    ["department_name", "department_location"],
                    [department_name, department_location],
                    "department_id",
                    dep_id
                )
                st.success("Department Updated!")
                st.rerun()
            if delete_btn:
                db.delete_row("department", "department_id", dep_id)
                st.success("Department Deleted!")
                st.rerun()
else:
    st.warning("You can only View Departments.")