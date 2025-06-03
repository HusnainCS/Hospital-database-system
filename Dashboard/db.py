# db.py

import psycopg2
import streamlit as st

@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=st.secrets["DB_HOST"],
        dbname=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASS"],
        sslmode='require'
    )

def execute_query(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def fetch_query(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        return cur.fetchall()
    except Exception as e:
        raise e
    finally:
        cur.close()

# ----- CRUD Helper Functions -----

def insert_row(table, columns, values):
    placeholders = ', '.join(['%s'] * len(values))
    columns_str = ', '.join(columns)
    query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
    execute_query(query, values)

def update_row(table, update_cols, update_vals, condition_col, condition_val):
    set_clause = ', '.join([f"{col} = %s" for col in update_cols])
    query = f"UPDATE {table} SET {set_clause} WHERE {condition_col} = %s"
    execute_query(query, update_vals + [condition_val])

def delete_row(table, condition_col, condition_val):
    query = f"DELETE FROM {table} WHERE {condition_col} = %s"
    execute_query(query, [condition_val])

def get_all_rows(table):
    query = f"SELECT * FROM {table}"
    return fetch_query(query)
