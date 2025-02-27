import streamlit as st
from navigation import make_sidebar

# Call the make_sidebar function to handle the sidebar and get the selected section
make_sidebar()

# Section: Appendix
st.title("Appendix")

st.markdown("""
### 1. Dataset Details
- Dataset: ISIC Archive, DermNet dataset, or another appropriate dataset.
- Preprocessing: Image resizing, normalization, splitting into training/validation/testing sets.

### 2. Machine Learning Model
- Model Types: Convolutional Neural Networks (ResNet, EfficientNet).
- Handling Data Imbalance: Oversampling, SMOTE.
- Performance Metrics: Accuracy, F1-score, precision, recall.

### 3. Libraries and Tools
- Libraries: TensorFlow, Keras, NumPy, Pandas, OpenCV, etc.
- Streamlit for web app development.

### 4. Deployment
- Install dependencies and use `streamlit run your_app.py` to start the app.
- Include model loading mechanism and inference function in the app.
""") 

st.title("Types of Skin Cancer")

st.markdown("""
### 1. Basal Cell Carcinoma (BCC)
- The most common type of skin cancer.
- Usually found in areas exposed to the sun, such as the head and neck.
- Grows slowly and rarely spreads.

### 2. Squamous Cell Carcinoma (SCC)
- The second most common type.
- Often appears on sun-exposed skin.
- Can grow into deeper layers of the skin and spread to other areas.

### 3. Melanoma
- The most dangerous type of skin cancer.
- Can develop from moles and spread quickly if not detected early.
- It may appear as an irregular mole with asymmetry, uneven borders, multiple colors, and a diameter larger than 6mm.

### 4. Merkel Cell Carcinoma (MCC)
- A rare but aggressive form.
- Tends to grow quickly and spread to other parts of the body.

### 5. Actinic Keratosis
- Precancerous patches that can turn into squamous cell carcinoma.
- Typically found on sun-exposed areas of the skin.
""")


st.title("Latest Research on Skin Cancer")

# Section 1: AI in Skin Cancer Detection
st.subheader("1. Artificial Intelligence in Skin Cancer Detection")
st.write("""
- Deep learning models, especially Convolutional Neural Networks (CNNs), are achieving dermatologist-level accuracy in detecting melanoma from dermatoscopic images.
- Research focuses on improving AI models for diverse skin tones and skin types.
""")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Dermatoscope.jpg/320px-Dermatoscope.jpg", caption="AI in Skin Cancer Detection", use_container_width=True)
st.markdown("[Click here to read the research paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7442686/)")

# Section 2: Personalized Cancer Therapy
st.subheader("2. Personalized Cancer Therapy")
st.write("""
- Research explores tailored treatment based on genetic mutations in melanoma.
- Immunotherapy and targeted therapies are showing promising results for advanced-stage melanomas.
""")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Oncology_nurse_wearing_PPE%2C_in_front_of_the_cytotoxic_drug_safety_cabinet%2C_at_Meridiaan_medical_center.jpg/320px-Oncology_nurse_wearing_PPE%2C_in_front_of_the_cytotoxic_drug_safety_cabinet%2C_at_Meridiaan_medical_center.jpg", caption="Personalized Cancer Therapy", use_container_width=True)
st.markdown("[Click here to read the research paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6068306/)")

# Section 3: Non-Invasive Diagnostic Methods
st.subheader("3. Non-Invasive Diagnostic Methods")
st.write("""
- Advances in non-invasive imaging techniques, such as reflectance confocal microscopy (RCM), enhance early detection accuracy.
- Research integrates these methods with AI-based diagnostics for faster results.
""")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Confocal_Scanning_Laser_Microscope.jpg/320px-Confocal_Scanning_Laser_Microscope.jpg", caption="Non-Invasive Diagnostic Methods", use_container_width=True)
st.markdown("[Click here to read the research paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6070861/)")

# Section 4: Public Awareness and Early Detection
st.subheader("4. Public Awareness and Early Detection")
st.write("""
- Emphasizes public health campaigns for regular skin checks, sun protection, and the role of self-examinations in early detection.
""")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Sunscreen_is_a_lotion%2C_spray%2C_gel_or_other_topical_product_that_absorbs_or_reflects_some_of_the_sun%27s_ultraviolet_radiation.jpg/320px-Sunscreen_is_a_lotion%2C_spray%2C_gel_or_other_topical_product_that_absorbs_or_reflects_some_of_the_sun%27s_ultraviolet_radiation.jpg", caption="Public Awareness and Early Detection", use_container_width=True)
st.markdown("[Click here to read more about public awareness and early detection](https://www.cancer.org/latest-news.html)")
