import streamlit as st
import db

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login to access this page.")
    st.stop()
    
def get_column_names():
    # You can hardcode or fetch dynamically for flexibility
    return ["supplier_name", "contact", "email"]

st.title("Supplier Management")
role = st.session_state.user["role"]

if role == "admin":
    suppliers = db.fetch_all("supplier")
    st.dataframe([dict(s) for s in suppliers])

    st.subheader("Add Supplier")
    with st.form("add_supplier_form"):
        supplier_name = st.text_input("Supplier Name")
        contact_no = st.text_input("Contact No")
        email = st.text_input("Email")

        submitted = st.form_submit_button("Add Patient")
        if submitted:
            db.insert_row(
                "supplier",
                ["supplier_name","contact_no","email",],
                [supplier_name, contact_no, email]
            )
            st.success("Supplier added!")
            st.rerun()

    st.subheader("Edit/Delete Patient")
    suppliers_ids = [sup["supplier_id"] for sup in suppliers]
    sup_id = st.selectbox("Select Supplier ID", suppliers_ids)
    selected = next((sup for sup in suppliers if sup["supplier_id"] == sup_id), None)
    if selected:
        with st.form("edit_supplier_form"):
            supplier_name = st.text_input("Supplier Name", selected["supplier_name"])
            contact_no = st.text_input("Contact No", selected["contact_no"])
            email = st.text_input("Email", selected["email"])

            update_btn = st.form_submit_button("Update Supplier")
            delete_btn = st.form_submit_button("Delete Supplier")
            if update_btn:
                db.update_row(
                    "supplier",
                    ["supplier_name", "contact_no","email"],
                    [supplier_name, contact_no, email,],
                    "supplier_id",
                    sup_id
                )
                st.success("Supplier Added!")
                st.rerun()
            if delete_btn:
                db.delete_row("supplier", "supplier_id", sup_id)
                st.success("Supplier deleted!")
                st.rerun()
else:
    st.warning("You do not have permission to view or manage Suppliers.")