import streamlit as st
from navigation import make_sidebar

make_sidebar()

st.title("What is skin cancer?")

st.write("")
st.write("""
    Skin cancer is one of the most common types of cancer, caused by the uncontrolled growth of abnormal skin cells. It occurs when the skin is exposed to harmful ultraviolet (UV) radiation from the sun or tanning beds, leading to DNA damage in skin cells. There are three main types of skin cancer: basal cell carcinoma (BCC), squamous cell carcinoma (SCC), and melanoma. While BCC and SCC are generally less aggressive, melanoma is the most dangerous form and can spread rapidly if not detected early.
""")

st.write("")
st.write("""
    Regular skin check-ups, using sunscreen, and avoiding excessive sun exposure can help prevent skin cancer. Early detection through self-examinations and professional screenings increases the chances of successful treatment. If you notice any unusual changes in moles, spots, or skin texture, it’s important to consult a healthcare professional for further evaluation.
""")

st.title("Skin Cancer Detection – ABCDE Method") 

st.write("Early detection of skin cancer can save lives. The **ABCDE rule** helps identify warning signs of melanoma:")  

st.markdown("""  
- **A - Asymmetry**: One half of the mole or spot does not match the other.  
- **B - Border**: Irregular, blurred, or jagged edges instead of smooth, even borders.  
- **C - Color**: Multiple colors (shades of brown, black, red, white, or blue) instead of a uniform color.  
- **D - Diameter**: Larger than **6mm** (about the size of a pencil eraser), though melanomas can be smaller.  
- **E - Evolving**: Changes in size, shape, color, or elevation over time. Any new symptoms like bleeding or itching are also concerning.  
""")

st.write("If you notice any of these signs, consult a healthcare professional for evaluation. Early diagnosis significantly improves treatment outcomes.")  

st.title("Our Project")

st.write("""
Welcome to our Skin Cancer Detection system. This web application aims to provide an easy-to-use platform for detecting potential skin cancer in lesions through machine learning.

By uploading an image of a skin lesion, users can receive an instant analysis of the lesion's characteristics. The system provides predictions and suggestions to help individuals identify potential skin cancer at an early stage. This tool is designed to raise awareness and encourage early diagnosis.

Key Features:
- **Image Submission**: Upload a clear image of your skin lesion for analysis.
- **Machine Learning-Based Prediction**: Receive a primary diagnosis based on the analysis.
- **Feedback Section**: Share your thoughts and improve the system’s performance.

Our goal is to empower users with the necessary tools to identify suspicious lesions and seek further professional advice.
""")
st.write("")

css ="""
    .st-key-one > div.stButton > button {
        background: linear-gradient(to right, #FF416C, #FF4B2B);
        border: none;
        border-radius: 40px;
        color: white;
        padding: 10px 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        transition: transform 0.2s;
        display: block;
        margin: 2rem auto;
    }

    .st-key-one button:hover {
        transform: scale(1.05);
    }
            
    .st-key-one > div.stButton > button p {
        font-size: 28px
    }
    """

st.html(f"<style>{css}</style>")


if st.button("Try Our App", key="one"):
    st.switch_page("pages/upload.py")

