import streamlit as st
import sqlite3
import os
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import numpy as np
import tensorflow as tf
from navigation import make_sidebar
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from utils import hide_streamlit_style

# Initialize session state for disclaimer and form submission
if "disclaimer_accepted" not in st.session_state:
    st.session_state.disclaimer_accepted = False  # Track if the user has accepted the disclaimer

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False  # Track if the form has been submitted

if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None

def split_text(canvas, text, max_width, font_name, font_size):
    lines = []
    if not text:
        return lines
    words = text.split()
    current_line = []
    current_width = 0
    space_width = canvas.stringWidth(' ', font_name, font_size)
    
    for word in words:
        word_width = canvas.stringWidth(word, font_name, font_size)
        if current_line:
            temp_width = current_width + space_width + word_width
        else:
            temp_width = word_width
            
        if temp_width <= max_width:
            current_line.append(word)
            current_width = temp_width
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width
    
    if current_line:
        lines.append(' '.join(current_line))
    return lines

st.set_page_config(page_title="Upload Page")

# Sidebar
make_sidebar()
hide_streamlit_style()

# Load the model with custom objects
model = tf.keras.models.load_model('efficientnet_gem_model_1.h5')

# Label mapping
label_map = {0: 'Actinic Keratoses and Intraepithelial Carcinoma', 
             1: 'Basal Cell Carcinoma', 
             2: 'Benign Keratosis', 
             3: 'Dermatofibroma', 
             4: 'Melanoma', 
             5: 'Melanocytic Nevus', 
             6: 'Vascular Lesions'}
predicted_class = None

# Display a title
st.title("Upload Skin Lesion Image")

# Disclaimer logic
if not st.session_state.disclaimer_accepted:
    st.markdown("""
        <h2>Disclaimer</h2>
        <p>This web application is not a substitute for professional medical advice, diagnosis, or treatment. It is designed for educational and informational purposes only. Always seek the advice of your physician or other qualified healthcare provider with any questions you may have regarding a medical condition.</p>
        <p><strong>Important:</strong> This tool is not intended to be used as a diagnostic tool. Consult with a healthcare provider for any concerns about your health.</p>
    """, unsafe_allow_html=True)

    if st.button("I agree"):
        st.session_state.disclaimer_accepted = True  # Update session state
        st.rerun()
else:
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT full_name FROM users WHERE username=?", (st.session_state.username,))
    user_data = c.fetchone()
    conn.close()

    if user_data and user_data[0]:
        st.session_state.form_submitted = True  # Skip form if data exists

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
                c.execute('''UPDATE users
                             SET full_name = ?, age = ?, gender = ?, family_history = ?, previous_conditions = ?, smoking_habits = ?, alcohol_consumption = ?, contact_email = ?
                             WHERE username = ?''',
                          (full_name, age, gender, family_history, previous_conditions, smoking_habits, alcohol_consumption, contact_email, st.session_state.username))
                conn.commit()
                conn.close()

                st.session_state.form_submitted = True
                st.success("Information updated successfully!")
                # No need for st.rerun() here; the state change will update the UI
            else:
                st.warning("Please fill in all required fields.")
    
    if st.session_state.form_submitted:
    # Once the form is submitted or data exists, show the image upload section
        st.header("Image Upload Guidelines")
        st.write("Before uploading your skin lesion image, please ensure that your image meets the following criteria for optimal analysis:")

        st.markdown("""
        - **Clear and Focused:** Ensure the image is sharp and in focus.
        - **Well-Lit:** The image should be taken in good lighting to avoid shadows or glare.
        - **Close-Up View:** The lesion should fill most of the image so that details can be accurately assessed.
        - **Accurate Color Representation:** Avoid filters or editing that may alter the true color of the lesion.
        - **Minimal Background Distractions:** A plain background helps to isolate the lesion for better analysis.
        """)
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
        
        if uploaded_file is not None:
            # Check if this is a new file upload
            current_file_name = uploaded_file.name
            if 'last_uploaded' not in st.session_state or st.session_state.last_uploaded != current_file_name:
                # New file, reset variables
                st.session_state.last_uploaded = current_file_name
                st.session_state.report_generated = False
                # Generate new filename
                st.session_state.pdf_filename = f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
            
            if not st.session_state.get('report_generated', False):
                # Process image and generate PDF
                img = Image.open(uploaded_file)
                st.image(img, caption='Uploaded Image', use_container_width=True)
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

            endpoint = "https://models.inference.ai.azure.com"
            model_name = "gpt-4o"
            token = os.environ["GITHUB_TOKEN"]
            if predicted_class is None:
                pass
            else:
                detected_cancer = label_map[predicted_class]
                client = ChatCompletionsClient(
                    endpoint=endpoint,
                    credential=AzureKeyCredential(token),
                )

                system_msg = SystemMessage(
                    "You are an expert AI assistant in dermatology and oncology. Provide accurate, detailed, and easy-to-understand medical information in a single short paragraph. "
                )

                user_msg = UserMessage(
                    f"I have detected {detected_cancer} in a patient's skin lesion image. Could you please provide a short overview of this condition in a single paragraph? "
                    "Include details such as a clear description of the cancer, common causes and risk factors, typical symptoms, diagnostic methods, treatment options (with potential side effects), prognosis, and any recommendations for follow-up care. "
                    "Also, mention any preventive measures or early detection strategies relevant to this cancer."
                )

                
                response = client.complete(
                    messages=[system_msg, user_msg],
                    max_tokens=1000,
                    model=model_name
                )

                st.write(response.choices[0].message.content)

                # Retrieve user info from database
                conn = sqlite3.connect("users.db")
                c_db = conn.cursor()
                c_db.execute("SELECT full_name, age, gender, family_history, previous_conditions, smoking_habits, alcohol_consumption, contact_email FROM users WHERE username=?", (st.session_state.username,))
                user_info = c_db.fetchone()
                conn.close()

                if user_info:
                    # Extract user info
                    full_name, age, gender, family_history, previous_conditions, smoking_habits, alcohol_consumption, contact_email = user_info
                    
                    # Handle empty fields
                    family_history = family_history or "None provided"
                    previous_conditions = previous_conditions or "None provided"

                    # Create PDF
                    pdf_buffer = io.BytesIO()
                    c_pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
                    width, height = letter
                    y = height - 40
                    c_pdf.setFont("Helvetica", 12)

                    # User Information
                    user_fields = [
                        f"Name: {full_name}",
                        f"Age: {age}",
                        f"Gender: {gender}",
                        f"Smoking Habits: {smoking_habits}",
                        f"Alcohol Consumption: {alcohol_consumption}",
                        f"Contact Email: {contact_email}"
                    ]
                    
                    for field in user_fields:
                        c_pdf.drawString(40, y, field)
                        y -= 20

                    # Medical History
                    c_pdf.drawString(40, y, "Family History:")
                    y -= 20
                    for line in split_text(c_pdf, family_history, 500, "Helvetica", 12):
                        c_pdf.drawString(60, y, line)
                        y -= 15
                    
                    c_pdf.drawString(40, y, "Previous Conditions:")
                    y -= 20
                    for line in split_text(c_pdf, previous_conditions, 500, "Helvetica", 12):
                        c_pdf.drawString(60, y, line)
                        y -= 15

                    # Image
                    uploaded_file.seek(0)
                    img = Image.open(uploaded_file)
                    img_width = 200
                    img_height = img_width * (img.height / img.width)
                    c_pdf.drawImage(ImageReader(img), 40, y-img_height, width=img_width, height=img_height)
                    y -= img_height + 30

                    # Results
                    c_pdf.setFont("Helvetica-Bold", 14)
                    c_pdf.drawString(40, y, "Diagnostic Results:")
                    y -= 20
                    c_pdf.setFont("Helvetica", 12)
                    # Draw prediction with underline
                    text = f"Prediction: {label_map[predicted_class]}"
                    c_pdf.drawString(40, y, text)
                    c_pdf.line(40, y-2, 40 + c_pdf.stringWidth(text, "Helvetica", 12), y-2)
                    y -= 20
                    
                    # Draw confidence with underline
                    text = f"Confidence: {confidence:.2%}"
                    c_pdf.drawString(40, y, text)
                    c_pdf.line(40, y-2, 40 + c_pdf.stringWidth(text, "Helvetica", 12), y-2)

                    y -= 20
                    c_pdf.drawString(40, y, "Analysis:")
                    y -= 20
                    explanation = response.choices[0].message.content
                    lines = split_text(c_pdf, explanation, max_width=500, font_name="Helvetica", font_size=14)
                    for line in lines:
                        c_pdf.drawString(40, y, line)
                        y -= 15

                    # Disclaimer
                    c_pdf.setFont("Helvetica-Oblique", 10)
                    c_pdf.drawString(40, 40, "Disclaimer: This report is not a replacement for professional medical diagnosis.")

                    c_pdf.save()
                    st.session_state.pdf_bytes = pdf_buffer.getvalue()
                    # Save PDF to file
                    report_dir = os.path.join("reports", st.session_state.username)
                    os.makedirs(report_dir, exist_ok=True)
                    filepath = os.path.join(report_dir, st.session_state.pdf_filename)
                    with open(filepath, "wb") as f:
                        f.write(st.session_state.pdf_bytes)
                    
                    # Mark report as generated
                    st.session_state.report_generated = True

            # Display download button if report has been generated
            if st.session_state.get('report_generated', False):
                st.download_button(
                    "Download Report",
                    data=st.session_state.pdf_bytes,
                    file_name=st.session_state.pdf_filename,
                    mime="application/pdf"
                )
            
            
st.write(st.session_state)