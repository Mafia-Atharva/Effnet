import streamlit as st
import sqlite3
import hashlib
from time import sleep
from navigation import make_sidebar

# Function to create the database and user table
def create_database():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Create the users table with the updated columns, including pdf_path
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE,
                 password TEXT,
                 pdf_path TEXT
                 full_name TEXT,
                 age INTEGER,
                 gender TEXT,
                 family_history TEXT,
                 previous_conditions TEXT,
                 smoking_habits TEXT,
                 alcohol_consumption TEXT,
                 contact_email TEXT
                 )''')

    conn.commit()
    conn.close()

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to register a user
def register_user(username, password, conn):
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        st.success("Registration successful. Please log in.")
    except sqlite3.IntegrityError:
        st.error("Username already exists. Please choose another.")

# Function to verify user login
def verify_user(username, password, conn):
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    return c.fetchone() is not None

# Function to check if user exists
def user_exists(username, conn):
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone() is not None

# Initialize database
create_database()
conn = sqlite3.connect("users.db", check_same_thread=False)

make_sidebar()

st.title("Skin Lesion Classification")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

if st.session_state["logged_in"]:
    st.success(f"Welcome, {st.session_state['username']}!")
    sleep(1)
else:
    choice = st.radio("Login / Register", ["Login", "Register"])

    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if verify_user(username, password, conn):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success(f"Logged in as {username}. Redirecting...")
                sleep(1)
                st.switch_page("pages/home.py")
            else:
                st.error("Incorrect username or password")

    elif choice == "Register":
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Register"):
            if not new_username.strip() or not new_password.strip():
                st.error("Username and password cannot be empty")
            elif user_exists(new_username, conn):
                st.error("Username already exists")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            else:
                register_user(new_username, new_password, conn)

st.write(st.session_state)

