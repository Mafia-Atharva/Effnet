import streamlit as st
import sqlite3
from navigation import make_sidebar
from PIL import Image
import numpy as np
import tensorflow as tf
from gem_layer import GeMPoolingLayer

# Initialize session state for disclaimer and form submission
if "disclaimer_accepted" not in st.session_state:
    st.session_state.disclaimer_accepted = False  # Track if the user has accepted the disclaimer

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False  # Track if the form has been submitted

# Sidebar
make_sidebar()

# Load the model with custom objects
model = tf.keras.models.load_model('efficientnet_gem_model_1.h5',
                                   custom_objects={'GeMPoolingLayer': GeMPoolingLayer})

# Label mapping
label_map = {0: 'akiec', 1: 'bcc', 2: 'bkl', 3: 'df', 4: 'mel', 5: 'nv', 6: 'vasc'}

# Display a title
st.title("Upload Skin Lesion Image")

# Disclaimer logic
if not st.session_state.disclaimer_accepted:
    st.markdown("""
        <h2>Disclaimer</h2>
        <p>This web application is not a substitute for professional medical advice, diagnosis, or treatment. It is designed for educational and informational purposes only. Always seek the advice of your physician or other qualified healthcare provider with any questions you may have regarding a medical condition.</p>
        <p><strong>Important:</strong> This tool is not intended to be used as a diagnostic tool. Consult with a healthcare provider for any concerns about your health.</p>
    """, unsafe_allow_html=True)

    # "I agree" button
    if st.button("I agree"):
        st.session_state.disclaimer_accepted = True  # Mark disclaimer as accepted
        st.rerun()  # Rerun the app to update the UI
else:
    # Show the form only if it hasn't been submitted
    if not st.session_state.form_submitted:
        with st.form("user_info_form"):
            full_name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=0, max_value=120, step=1)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            family_history = st.text_area("Family History (if any)")
            previous_conditions = st.text_area("Previous Medical Conditions (if any)")
            smoking_habits = st.selectbox("Smoking Habits", ["Non-smoker", "Occasional", "Regular"])
            alcohol_consumption = st.selectbox("Alcohol Consumption", ["Never", "Occasional", "Frequent"])
            contact_email = st.text_input("Contact Email")

            submit_button = st.form_submit_button("Submit")

        if submit_button:
            if full_name and contact_email:
                conn = sqlite3.connect("users.db")
                c = conn.cursor()
                c.execute("SELECT username FROM users WHERE username=?", (st.session_state.username,))
                user_exists = c.fetchone()

                if user_exists:
                    # Update user data
                    c.execute('''UPDATE users
                                 SET full_name = ?, age = ?, gender = ?, family_history = ?, previous_conditions = ?, smoking_habits = ?, alcohol_consumption = ?, contact_email = ?
                                 WHERE username = ?''',
                              (full_name, age, gender, family_history, previous_conditions, smoking_habits, alcohol_consumption, contact_email, st.session_state.username))
                    conn.commit()
                    conn.close()

                    st.session_state.form_submitted = True  # Mark the form as submitted
                    st.success("Information updated successfully!")
                    st.rerun()  # Rerun the app to update the UI
                else:
                    st.error("Error: Username not found. Please register first.")
            else:
                st.warning("Please fill in all required fields.")
    else:
        # Once the form is submitted, show the image upload section
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            img = Image.open(uploaded_file)
            st.image(img, caption='Uploaded Image', use_column_width=True)
            st.write("Classifying...")

            # Preprocess the image
            img = img.resize((224, 224))
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Make prediction
            predictions = model.predict(img_array)
            predicted_class = np.argmax(predictions, axis=1)[0]
            confidence = np.max(predictions)

            # Display results
            st.write(f"Predicted class: {label_map[predicted_class]}")
            st.write(f"Confidence: {confidence:.2f}")

# Debugging: Display session state
st.write(st.session_state)