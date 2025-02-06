import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
from gem_layer import GeMPoolingLayer  # Importing the custom GeM layer

# Load the model with custom objects
model = tf.keras.models.load_model('efficientnet_gem_model_1.h5',
                                   custom_objects={'GeMPoolingLayer': GeMPoolingLayer})

# Label mapping
label_map = {0: 'akiec', 1: 'bcc', 2: 'bkl', 3: 'df', 4: 'mel', 5: 'nv', 6: 'vasc'}

# Streamlit Interface
st.title("Skin Lesion Classification")
st.write("Upload an image of a skin lesion to classify it.")

# Image upload
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
