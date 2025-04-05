import os
import joblib
import requests
import cv2
import numpy as np
import pandas as pd
import hashlib
from flask import Flask, request, jsonify
from pyzbar.pyzbar import decode
from urllib.parse import urlparse

app = Flask(__name__)

# Load trained model
model = joblib.load("hospital_url_xgb.pkl")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Path to the original QR code image
ORIGINAL_QR_PATH = "original_qr.png"

# Expected real URL (Update this with your correct hospital URL)
EXPECTED_HOSPITAL_URL = "https://real-hospital.com/certificate/12345"

# Common URL shorteners
SHORTENED_DOMAINS = ["qrco.de", "bit.ly", "goo.gl", "t.co", "tinyurl.com"]

def is_shortened_url(url):
    """Check if the given URL is from a known URL shortener."""
    parsed_url = urlparse(url)
    return any(shortened in parsed_url.netloc for shortened in SHORTENED_DOMAINS)

def resolve_shortened_url(shortened_url):
    """Resolve a shortened URL to its original destination."""
    try:
        response = requests.get(shortened_url, allow_redirects=True)
        return response.url
    except requests.exceptions.RequestException:
        return None

def extract_url_features(url):
    """Extract numerical features from a URL for prediction."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path

    features = {
        "domain_length": len(domain),
        "num_subdomains": domain.count('.'),
        "contains_hospital": int("hospital" in domain.lower()),
        "contains_medical": int("medical" in domain.lower()),
        "contains_clinic": int("clinic" in domain.lower()),
        "path_length": len(path)
    }

    print(f"[DEBUG] Extracted Features: {features}")  # Debugging
    return features

def predict_url(url):
    """Predict whether a given URL is real or fake using the trained model."""
    if model is None:
        return "Model not loaded"

    features = extract_url_features(url)
    features_df = pd.DataFrame([features])
    
    prediction = model.predict(features_df)

    print(f"[DEBUG] URL: {url}, Prediction Result: {prediction[0]}")  # Debugging
    return "Real Hospital URL" if prediction[0] == 1 else "Fake Hospital URL"

def read_qr_code(image_path):
    """Extract a URL from a QR code in an image."""
    try:
        img = cv2.imread(image_path)
        if img is None:
            print("[ERROR] Could not load image for QR code decoding")
            return None

        decoded_objects = decode(img)
        for obj in decoded_objects:
            extracted_url = obj.data.decode("utf-8")
            print(f"[DEBUG] Extracted QR Code URL: {extracted_url}")  # Debugging
            return extracted_url

    except Exception as e:
        print(f"[ERROR] QR Code Reading Failed: {e}")

    return None

def get_image_hash(image_path):
    """Generate a hash for an image to detect modifications."""
    try:
        with open(image_path, "rb") as f:
            img_hash = hashlib.sha256(f.read()).hexdigest()
            print(f"[DEBUG] Image Hash ({image_path}): {img_hash}")  # Debugging
            return img_hash
    except Exception as e:
        print(f"[ERROR] Hashing failed for {image_path}: {e}")
        return None

def is_qr_tampered(uploaded_qr_path):
    """Check if the uploaded QR code is tampered using hash comparison."""
    original_qr_hash = get_image_hash(ORIGINAL_QR_PATH)
    uploaded_qr_hash = get_image_hash(uploaded_qr_path)

    if original_qr_hash and uploaded_qr_hash:
        print(f"[DEBUG] Original QR Hash: {original_qr_hash}")
        print(f"[DEBUG] Uploaded QR Hash: {uploaded_qr_hash}")

        return original_qr_hash != uploaded_qr_hash
    return True  # Assume tampering if hash comparison fails

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint to check if a hospital certificate QR is real or fake."""
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    filepath = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(filepath)

    # Step 1: Detect tampered QR image using hash comparison
    if is_qr_tampered(filepath):
        return jsonify({"prediction": "Fake Certificate (Tampered QR Image)"}), 200

    # Step 2: Extract the URL from the QR code
    url = read_qr_code(filepath)

    if not url:
        return jsonify({"error": "No QR code detected"}), 400

    # Step 3: Check if extracted URL matches expected hospital URL
    if url == EXPECTED_HOSPITAL_URL:
        return jsonify({"url": url, "prediction": "Real Hospital URL"}), 200

    # Step 4: If the URL is shortened, resolve it
    if is_shortened_url(url):
        original_url = resolve_shortened_url(url)
        if not original_url:
            return jsonify({"error": "Could not resolve shortened URL"}), 400
        url = original_url

    # Step 5: Predict if the resolved URL is real or fake using ML model
    prediction = predict_url(url)

    return jsonify({"url": url, "prediction": prediction})

if __name__ == "__main__":
    app.run(debug=True)