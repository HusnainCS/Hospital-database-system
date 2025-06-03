import streamlit as st
import db
import pandas as pd

# --------- LOGIN CHECK ----------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login to access the payment page.")
    st.stop()


st.title("Payments")

role = st.session_state.user["role"]

# ---------- Helper: Get patients for dropdown ----------
def get_patients():
    query = "SELECT patient_id, first_name, last_name FROM patient ORDER BY created_at DESC LIMIT 100"
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": row[0], "name": f"{row[1]} {row[2]}"} for row in rows]

# ---------- Helper: Get recent payments ----------
def get_recent_payments(limit=5000):
    query = f"SELECT * FROM payment ORDER BY payment_id DESC LIMIT {limit}"
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return pd.DataFrame(rows, columns=columns)

# ---------- USER: Make Payment ----------
if role == "user":
    st.subheader("Make a Payment")
    patients = get_patients()
    with st.form("make_payment_form"):
        patient_options = [f"{p['id']} - {p['name']}" for p in patients]
        patient_choice = st.selectbox("Select Patient", patient_options)
        amount = st.number_input("Amount", min_value=0.0, step=0.01, format="%.2f")
        submitted = st.form_submit_button("Submit Payment")
        if submitted:
            patient_id = int(patient_choice.split(" - ")[0])
            payment_status = "Paid"  # Always set to Paid on submission
            db.insert_row(
                "payment",
                ["patient_id", "amount", "payment_status"],
                [patient_id, amount, payment_status]
            )
            st.success("Payment submitted successfully!")

# ---------- ADMIN: View Payments ----------
elif role == "admin":
    st.subheader("All Payment Records")
    payments = get_recent_payments(5000)
    if not payments.empty:
        display_cols = [c for c in ['payment_id', 'patient_id', 'amount', 'payment_status', 'created_at'] if c in payments.columns]
        st.dataframe(payments[display_cols], hide_index=True, use_container_width=True)
    else:
        st.info("No payment records found.")

# ---------- Other roles ----------
else:
    st.warning("You do not have permission to access the payment page.")