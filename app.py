import streamlit as st
import sqlite3
import hashlib
from navigation import make_sidebar
from time import sleep

st.set_page_config(page_title="Register/Login")

# Function to create the database and user table
def create_database():
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        # Create the users table with the updated columns, including pdf_path
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT UNIQUE,
                     password TEXT,
                     pdf_path TEXT,
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

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to register a user
def register_user(username, password, conn):
    try:
        with conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
    except sqlite3.IntegrityError:
        st.error("Username already exists. Please choose another.")

# Function to verify user login
def verify_user(username, password, conn):
    with conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password(password)))
        return c.fetchone() is not None

# Function to check if user exists
def user_exists(username, conn):
    with conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        return c.fetchone() is not None

# Initialize database
create_database()
conn = sqlite3.connect("users.db", check_same_thread=False)

make_sidebar()

st.title("Skin Lesion Classification")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

if st.session_state["logged_in"]:
    st.success(f"Logged in as {st.session_state['username']}")
    sleep(1)
    st.switch_page("pages/home.py")  # Redirect to the home page
else:
    choice = st.radio("Login / Register", ["Login", "Register"])

    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if not username.strip() or not password.strip():
                st.error("Username and password cannot be empty")
            elif verify_user(username, password, conn):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success(f"Logged in as {username}. Redirecting...")
                sleep(1)
                st.switch_page("pages/home.py")  # Redirect to the home page
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
                st.session_state["logged_in"] = True
                st.session_state["username"] = new_username
                st.success("Registration successful. Redirecting...")
                sleep(1)
                st.switch_page("pages/home.py")  # Redirect to the home page



hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)