import streamlit as st
import sqlite3
import hashlib
import time
from st_pages import Page, show_pages

def create_database():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE,
                 password TEXT,
                 pdf_path TEXT)''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, conn):
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        st.success("Registration successful. Please log in.")
    except sqlite3.IntegrityError:
        st.error("Username already exists. Please choose another.")

def verify_user(username, password, conn):
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    return c.fetchone() is not None

def user_exists(username, conn):
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone() is not None

# Initialize database
create_database()
conn = sqlite3.connect("users.db", check_same_thread=False)

st.title("Skin Lesion Classification")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""

# If the user is authenticated, show the logout button and navigation
if st.session_state.get("authenticated", False):
    # Show the logout button in the sidebar
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"authenticated": False}))

    # Show navigation after successful login
    show_pages([
        Page("app.py", "Home", "🏠"),
        Page("upload.py", "Upload Image", "📷"),
        Page("reports.py", "Reports", "📄"),
    ])

else:
    with st.container():
        choice = st.radio("Login / Register", ["Login", "Register"])

        if choice == "Login":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                if verify_user(username, password, conn):
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.success("Logged in as {}. Redirecting to the app".format(username))
                    time.sleep(3)
                    st.rerun()  # Use this instead of st.rerun() in the main script
                else:
                    st.error("Incorrect username or password")

        elif choice == "Register":
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            if st.button("Register"):
                if new_username.strip() == "" or new_password.strip() == "":
                    st.error("Username and password cannot be empty")
                elif user_exists(new_username, conn):
                    st.error("Username already exists")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    register_user(new_username, new_password, conn)

st.write(st.session_state)


# else:
#     st.sidebar.title("Navigation")
#     if st.sidebar.button("Home"):
#         st.write(f"Welcome, {st.session_state['username']}!")
#     if st.sidebar.button("Upload Image"):
#         uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
#         # if uploaded_file is not None:
#             # img = Image.open(uploaded_file)
#             # st.image(img, caption='Uploaded Image', use_column_width=True)
#             # st.write("Classifying...")

#             # img = img.resize((224, 224))
#             # img_array = np.array(img) / 255.0
#             # img_array = np.expand_dims(img_array, axis=0)

#             # predictions = model.predict(img_array)
#             # predicted_class = np.argmax(predictions, axis=1)[0]
#             # confidence = np.max(predictions)

#             # st.write(f"Predicted class: {label_map[predicted_class]}")
#             # st.write(f"Confidence: {confidence:.2f}")
#     if st.sidebar.button("Reports"):
#         st.write("Reports page - Under development.")
#     if st.sidebar.button("Logout"):
#         st.session_state["authenticated"] = False
#         st.rerun()
