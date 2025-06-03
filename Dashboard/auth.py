import db

def login(username, password):
    user = db.fetch_one("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    if user:
        return {"username": user["username"], "role": user["role"]}
    else:
        return None