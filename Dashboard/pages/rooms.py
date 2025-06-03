import streamlit as st
import db
import pandas as pd

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login to access this page.")
    st.stop()
    
st.title("Room Management")
role = st.session_state.user["role"]

def get_recent_rooms(limit=20):
    query = f"SELECT * FROM room ORDER BY room_id DESC LIMIT {limit}"
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return pd.DataFrame(rows, columns=columns)

def get_patients():
    query = "SELECT patient_id, first_name, last_name FROM patient ORDER BY created_at DESC LIMIT 100"
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": row[0], "name": f"{row[1]} {row[2]}"} for row in rows]

rooms = get_recent_rooms(20)
display_cols = [c for c in ['room_number', 'room_type', 'status', 'patient_id', 'created_at'] if c in rooms.columns]
st.dataframe(rooms[display_cols], hide_index=True)

if role == "admin":
    st.subheader("Add Room")
    patients = get_patients()
    with st.form("add_room_form"):
        room_number = st.number_input("Room Number", min_value=1, step=1)
        room_type = st.selectbox("Room Type", ["General", "ICU", "Private", "Semi-Private"])
        status = st.selectbox("Status", ["Available", "Occupied", "Cleaning", "Maintenance"])
        patient_options = ["Unassigned"] + [f"{p['id']} - {p['name']}" for p in patients]
        patient_choice = st.selectbox("Assign Patient (optional)", patient_options)
        submitted = st.form_submit_button("Add Room")  # <--- This is required!
        if submitted:
            patient_id = None
            if patient_choice != "Unassigned":
                patient_id = int(patient_choice.split(" - ")[0])
            db.insert_row(
                "room",
                ["room_number", "room_type", "status", "patient_id"],
                [room_number, room_type, status, patient_id]
            )
            st.success("Room added!")
            st.experimental_rerun()

    st.subheader("Edit/Delete Room")
    room_ids = rooms["room_id"].tolist()
    if room_ids:
        room_id = st.selectbox("Select Room ID", room_ids)
        selected = rooms[rooms["room_id"] == room_id].iloc[0]
        with st.form("edit_room_form"):
            room_number = st.number_input("Room Number", min_value=1, step=1, value=int(selected["room_number"]))
            room_type_list = ["General", "ICU", "Private", "Semi-Private"]
            room_type_index = room_type_list.index(selected["room_type"]) if selected["room_type"] in room_type_list else 0
            room_type = st.selectbox("Room Type", room_type_list, index=room_type_index)

            status_list = ["Available", "Occupied", "Cleaning", "Maintenance"]
            status_index = status_list.index(selected["status"]) if selected["status"] in status_list else 0
            status = st.selectbox("Status", status_list, index=status_index)

            patients = get_patients()
            patient_options = ["Unassigned"] + [f"{p['id']} - {p['name']}" for p in patients]
            patient_preselect = "Unassigned"
            if pd.notnull(selected["patient_id"]):
                for p in patients:
                    if p["id"] == selected["patient_id"]:
                        patient_preselect = f"{p['id']} - {p['name']}"
                        break
            patient_index = patient_options.index(patient_preselect) if patient_preselect in patient_options else 0
            patient_choice = st.selectbox("Assign Patient (optional)", patient_options, index=patient_index)
            update_btn = st.form_submit_button("Update Room")
            delete_btn = st.form_submit_button("Delete Room")
            if update_btn:
                patient_id = None
                if patient_choice != "Unassigned":
                    patient_id = int(patient_choice.split(" - ")[0])
                db.update_row(
                    "room",
                    ["room_number", "room_type", "status", "patient_id"],
                    [room_number, room_type, status, patient_id],
                    "room_id",
                    room_id
                )
                st.success("Room updated!")
                st.experimental_rerun()
            if delete_btn:
                db.delete_row("room", "room_id", room_id)
                st.success("Room deleted!")
                st.experimental_rerun()
else:
    st.info("You have view-only access to room information.")