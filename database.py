import sqlite3
import bcrypt

DB_NAME = "users.db"

def init_db():
    """Create the users table if it does not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password):
    """Hash password and insert a new user."""
    if not username or not password:
        return False, "Username and password cannot be empty."

    # Hash the password using bcrypt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        return True, "Registration successful! You can now log in."
    except sqlite3.IntegrityError:
        return False, "Username already exists. Please choose another."

def verify_user(username, password):
    """Verify username and password against the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row and bcrypt.checkpw(password.encode('utf-8'), row[0]):
        return True, "Login successful!"
    return False, "Invalid username or password."

if __name__ == "__main__":
    init_db()
    print("Database initialized.")