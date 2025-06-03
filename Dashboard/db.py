import psycopg2
import psycopg2.extras
import streamlit as st

def get_connection():
    return psycopg2.connect(
        host=st.secrets["DB_HOST"],
        dbname=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASS"],
        sslmode='require'
    )

def fetch_query(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params or ())
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

def execute_query(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params or ())
    conn.commit()
    cur.close()
    conn.close()

def fetch_all(table, extra=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table} {extra}")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

def fetch_one(query, params=None):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query, params or ())
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def fetch_by_id(table, id_column, obj_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f"SELECT * FROM {table} WHERE {id_column}=%s", (obj_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def insert_row(table, columns, values):
    conn = get_connection()
    cur = conn.cursor()
    cols = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(values))
    cur.execute(f"INSERT INTO {table} ({cols}) VALUES ({placeholders})", values)
    conn.commit()
    cur.close()
    conn.close()

def update_row(table, columns, values, id_column, obj_id):
    conn = get_connection()
    cur = conn.cursor()
    set_clause = ', '.join([f"{col}=%s" for col in columns])
    cur.execute(
        f"UPDATE {table} SET {set_clause} WHERE {id_column}=%s",
        (*values, obj_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_row(table, id_column, obj_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table} WHERE {id_column}=%s", (obj_id,))
    conn.commit()
    cur.close()
    conn.close()
