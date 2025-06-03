import streamlit as st
import db

if (
    "logged_in" not in st.session_state
    or not st.session_state.logged_in
    or st.session_state.user.get("role") != "admin"
):
    st.warning("Admin access only.")
    st.stop()

st.title("Pending Appointment Requests")

pending = db.fetch_query(
    "SELECT * FROM appointment_request WHERE status = 'Pending' ORDER BY created_at ASC"
)

if pending:
    for req in pending:
        st.markdown(
            f"""
            **Request #{req['request_id']}**

            - **Patient Name:** {req['first_name']} {req['last_name']}
            - **Doctor ID:** {req['doctor_id']}
            - **Date:** {req['requested_date']}
            - **Time:** {req['requested_time']}
            - **Reason:** {req['reason']}
            """
        )
        with st.form(f"form_{req['request_id']}"):
            admin_notes = st.text_area(
                "Admin Notes", value=req.get("admin_notes") or ""
            )
            col1, col2 = st.columns(2)
            with col1:
                approve_btn = st.form_submit_button("Approve")
            with col2:
                reject_btn = st.form_submit_button("Reject")
            if approve_btn:
                db.execute_query(
                    "UPDATE appointment_request SET status = %s, admin_notes = %s WHERE request_id = %s",
                    ("Approved", admin_notes, req["request_id"]),
                )
                st.success("Request approved!")
                st.rerun()
            if reject_btn:
                db.execute_query(
                    "UPDATE appointment_request SET status = %s, admin_notes = %s WHERE request_id = %s",
                    ("Rejected", admin_notes, req["request_id"]),
                )
                st.warning("Request rejected.")
                st.rerun()
else:
    st.info("No pending appointment requests.")