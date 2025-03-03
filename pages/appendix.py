import streamlit as st
from navigation import make_sidebar
from utils import hide_streamlit_style

st.set_page_config(page_title="Appendix")

# Call the make_sidebar function to handle the sidebar and get the selected section
make_sidebar()
hide_streamlit_style()

# Section: Appendix
st.title("Skin Cancer Detection Project Overview")

st.markdown("""
### 1. Dataset Details
- **Dataset**: HAM10000 dataset, which contains a large collection of dermatoscopic images for skin lesion classification.
- **Preprocessing**: Image resizing, normalization, splitting into training/validation/testing sets.

### 2. Machine Learning Model
- **Model Types**: Convolutional Neural Networks (ResNet, EfficientNet).
- **Handling Data Imbalance**: Oversampling, SMOTE.
- **Performance Metrics**: Accuracy, F1-score, precision, recall.

### 3. Libraries and Tools
- **Libraries**: TensorFlow, Keras, NumPy, Pandas, OpenCV, etc.
- **Streamlit** for web app development.

### 4. Deployment
- Install dependencies and use `streamlit run your_app.py` to start the app.
- Include model loading mechanism and inference function in the app.
""")

# Section: Types of Skin Cancer
st.title("Types of Skin Cancer")

skin_cancers = {
    "Basal Cell Carcinoma (BCC)": "The most common type of skin cancer. Usually found in areas exposed to the sun, such as the head and neck. Grows slowly and rarely spreads.",
    "Squamous Cell Carcinoma (SCC)": "The second most common type. Often appears on sun-exposed skin. Can grow into deeper layers of the skin and spread to other areas.",
    "Melanoma": "The most dangerous type of skin cancer. Can develop from moles and spread quickly if not detected early. Appears as an irregular mole with asymmetry, uneven borders, multiple colors, and a diameter larger than 6mm.",
    "Merkel Cell Carcinoma (MCC)": "A rare but aggressive form. Tends to grow quickly and spread to other parts of the body.",
    "Actinic Keratosis": "Precancerous patches that can turn into squamous cell carcinoma. Typically found on sun-exposed areas of the skin."
}

for cancer_type, description in skin_cancers.items():
    st.subheader(cancer_type)
    st.write(description)

# Section: Latest Research on Skin Cancer
st.title("Latest Research on Skin Cancer")

research_sections = [
    {
        "title": "1. Artificial Intelligence in Skin Cancer Detection",
        "content": "Deep learning models, especially Convolutional Neural Networks (CNNs), are achieving dermatologist-level accuracy in detecting melanoma from dermatoscopic images. Research focuses on improving AI models for diverse skin tones and skin types.",
        "image": "images/cancer1.jpeg",
        "caption": "AI in Skin Cancer Detection",
        "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7442686/"
    },
    {
        "title": "2. Personalized Cancer Therapy",
        "content": "Research explores tailored treatment based on genetic mutations in melanoma. Immunotherapy and targeted therapies are showing promising results for advanced-stage melanomas.",
        "image": "images/personalized .jpeg",
        "caption": "Personalized Cancer Therapy",
        "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6068306/"
    },
    {
        "title": "3. Non-Invasive Diagnostic Methods",
        "content": "Advances in non-invasive imaging techniques, such as reflectance confocal microscopy (RCM), enhance early detection accuracy. Research integrates these methods with AI-based diagnostics for faster results.",
        "image": "images/non inavse tech.jpeg",
        "caption": "Non-Invasive Diagnostic Methods",
        "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6070861/"
    },
    {
        "title": "4. Public Awareness and Early Detection",
        "content": "Emphasizes public health campaigns for regular skin checks, sun protection, and the role of self-examinations in early detection.",
        "image": "images/skin-cancer-awareness.jpeg",
        "caption": "Public Awareness and Early Detection",
        "link": "https://www.cancer.org/latest-news.html"
    }
]

for section in research_sections:
    st.subheader(section["title"])
    st.write(section["content"])
    st.image(section["image"], caption=section["caption"], use_container_width=True)
    st.markdown(f"[Click here to read the research paper]({section['link']})")

# Section: Project Team
st.title("Project Team")

# Guide's Section
st.subheader("Guide")
st.image("https://example.com/path_to_guide_photo.jpg", caption="Dr. D.P.Gaikwad", use_container_width=True)
st.markdown("""
**Dr. D.P.Gaikwad**  
Professor, Department of Computer Engineering  
[Aissms Coe, Pune]  
Email: [dpgaikwad@aissmscoe.com]
""")

# Project Members Section
st.subheader("Project Members")
project_members = ["Harshwardhan Gaikwad", "Atharva Bhosale", "Krushnakant Babalsure", "Tushar Basugade"]

for member in project_members:
    st.markdown(f"- {member}")


