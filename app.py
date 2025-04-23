import streamlit as st
import pickle
import re
from urllib.parse import urlparse

# Load the saved model
filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

# Define the preprocess_url function
def preprocess_url(url):

    # Extract features from the URL
    features = [
        1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,  # Have_IP
        1 if '@' in url else 0,  # Have_At
        1 if len(url) > 75 else 0,  # URL_Length
        url.count('/') - 2 if url.count('/') > 2 else 0,  # URL_Depth
        1 if '//' in urlparse(url).path else 0,  # Redirection
        1 if url.startswith("https") else 0,  # https_Domain
        1 if any(shortener in url for shortener in ["tinyurl", "bit.ly", "goo.gl"]) else 0,  # TinyURL
        1 if '-' in urlparse(url).netloc else 0,  # Prefix/Suffix
        0,  # DNS_Record (placeholder, requires external check)
        1 if "traffic" in url else 0,  # Web_Traffic (simplified heuristic)
        1,  # Domain_Age (placeholder, requires external check)
        1,  # Domain_End (placeholder, requires external check)
        1 if '<iframe' in url.lower() else 0,  # iFrame (simplified heuristic)
        1 if 'onmouseover' in url.lower() else 0,  # Mouse_Over
        1 if 'right-click' in url.lower() else 0,  # Right_Click
        1 if url.count('//') > 1 else 0  # Web_Forwards
    ]
    return features

# Define the prediction function
def predict_url(url):
    # Preprocess the URL
    url_features = preprocess_url(url)
    # Make prediction
    prediction = loaded_model.predict([url_features])
    return prediction[0]

# Streamlit app
st.title("🔍 URL Maliciousness Predictor")

# Input URL from user
url = st.text_input("🌐 Enter a URL to check:")

if st.button("🚦 Predict"):
    if url:
        # Get prediction
        prediction = predict_url(url)
        # Display result
        if prediction == 1:
            st.error(f"❌ The URL '{url}' is predicted to be Malicious.")
        else:
            st.success(f"✅ The URL '{url}' is predicted to be Benign.")
    else:
        st.warning("⚠️ Please enter a URL.")