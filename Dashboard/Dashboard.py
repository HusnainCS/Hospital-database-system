import streamlit as st
import auth
import db
import pandas as pd

st.set_page_config(page_title="Hospital Dashboard", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

def login_screen():
    st.title("Hospital Dashboard Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = auth.login(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success(f"Welcome, {user['username']}!")
            st.rerun()
        else:
            st.error("Please Check Username or Password.")

def get_recent(table, sort_col, limit=5):
    # Efficient: Only fetch the latest `limit` records
    query = f"SELECT * FROM {table} ORDER BY {sort_col} DESC LIMIT {limit}"
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return pd.DataFrame(rows, columns=columns)

def main():
    if not st.session_state.logged_in:
        login_screen()
        return

    st.title("🏥 Utmanziy Hospital Management")
    st.markdown("---")
    
    # Key Metrics (only numbers, details moved below)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Patients Treated", "100,000+")
    with col2:
        st.metric("Doctors", "130")
    with col3:
        st.metric("Departments", "50")
    with col4:
        st.metric("Locations", "3")

    st.markdown("---")

    # Beautiful Overview Section (Patients, Doctors, Departments, Locations, About)
    st.markdown("""
    <div style="background-color:#f8fafc;padding:24px 32px 24px 32px;border-radius:8px;">
        <h2 style="color:#1565c0;margin-bottom:4px;">Hospital Overview</h2>
        <div style="font-size:18px;">
            <b>👥 Patients Treated:</b> 100,000+<br>
            <b>🩺 Doctors & Specialties:</b><br>
            &nbsp;&nbsp;- Dr. Sara Ahsan <i>(Dentist)</i>, <b>Timing:</b> 09:00 AM - 02:00 PM<br>
            &nbsp;&nbsp;- Dr. Usman Khalid <i>(General Surgeon)</i>, <b>Timing:</b> 10:00 AM - 02:00 PM<br>
            &nbsp;&nbsp;- Dr. Ali Raza <i>(Orthopedic)</i>, <b>Timing:</b> 12:00 AM - 04:00 PM<br>
            &nbsp;&nbsp;- Dr. Maria Iqbal <i>(Cardiologist)</i>, <b>Timing:</b> 09:00 AM - 01:00 PM<br>
            &nbsp;&nbsp;- Dr. Farhan Ahmed <i>(Neurologist)</i>, <b>Timing:</b> 02:00 AM - 05:00 PM<br>
            <br>
            <b>🏥 Departments:</b> Dentistry, General Surgery, Orthopedics, Cardiology, Neurology<br>
            <b>📍 Locations:</b> Main Campus (123 Main Street), Branch A (456 North Ave), Branch B (789 South Road)<br>
            <br>
            <b>About Hospital:</b> <br>
            Utmanziy Hospital is a leading multi-specialty hospital with state-of-the-art facilities, 24/7 emergency, advanced diagnostics, and compassionate care. Thank you for trusting us!
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Efficient Recent Activity (only latest 5 records)
    st.subheader("Recent Activity")
    recent_patients = get_recent("patient", "created_at", limit=5)
    recent_appointments = get_recent("appointment", "created_at", limit=5)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Recent Patients**")
        display_cols = [c for c in ['first_name', 'last_name', 'gender', 'created_at'] if c in recent_patients.columns]
        st.dataframe(recent_patients[display_cols], hide_index=True)
    with col2:
        st.write("**Recent Appointments**")
        display_cols = [c for c in ['appointment_date', 'appointment_time', 'appointment_status', 'created_at'] if c in recent_appointments.columns]
        st.dataframe(recent_appointments[display_cols], hide_index=True)

with st.sidebar:
    st.markdown("---")
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

if __name__ == "__main__":
    main()