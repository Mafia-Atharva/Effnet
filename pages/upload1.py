import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image

# Load the trained model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("test_eff.h5")

model = load_model()

# Define class labels (update according to your dataset)
class_labels = ["akiec", "bcc", "bkl", "df", "mel", "nv", "vasc"]

# Streamlit app UI
st.title("Skin Cancer Classification using EfficientNetB0")
st.write("Upload an image to classify the type of skin lesion.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Preprocess the image
    image = Image.open(uploaded_file).resize((224, 224))
    img_array = np.array(image) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Expand dimensions

    # Predict
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)[0]
    confidence = np.max(prediction)

    # Display the result
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write(f"**Predicted Class:** {class_labels[predicted_class]}")
    st.write(f"**Confidence:** {confidence:.2f}")
