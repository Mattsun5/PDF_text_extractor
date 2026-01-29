# database.py
import sqlite3
import datetime
import hashlib

DB_NAME = "extractions_log.db"

def hash_password(password):
    """Hashes the password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def setup_database():
    """Sets up the database with users and extractions tables."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    # Create extractions table with a foreign key to users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS extractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            extracted_text TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    # Create a test user if one doesn't exist
    cursor.execute("SELECT * FROM users WHERE email = ?", ('test@example.com',))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            ('test@example.com', hash_password('password123'))
        )
    conn.commit()
    conn.close()

def add_user(email, password):
    """Adds a new user to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError: # Email already exists
        return False
    finally:
        conn.close()

def verify_user(email, password):
    """Verifies user credentials."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    if user and user[1] == hash_password(password):
        return user[0] # Return user ID
    return None

# --- THIS IS THE CORRECTED FUNCTION ---
def add_extraction(user_id, filename, extracted_text):
    """Adds an extraction record for a specific user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now()
    # THE FIX: Added a fourth '?' to match the four columns
    cursor.execute(
        "INSERT INTO extractions (user_id, filename, extracted_text, timestamp) VALUES (?, ?, ?, ?)",
        (user_id, filename, extracted_text, timestamp)
    )
    conn.commit()
    conn.close()
# --- END OF CORRECTED FUNCTION ---

def get_user_extractions(user_id):
    """Retrieves all extraction records for a specific user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, filename, timestamp FROM extractions WHERE user_id = ? ORDER BY timestamp DESC",
        (user_id,)
    )
    records = cursor.fetchall()
    conn.close()
    return records