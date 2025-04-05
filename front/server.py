import os
import cv2
import joblib
import pytesseract
import numpy as np
import requests
import hashlib
from flask import Flask, request, jsonify
from PIL import Image
from pyzbar.pyzbar import decode
from urllib.parse import urlparse
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the XGBoost model
def load_model():
    return joblib.load("hospital_url_xgb.pkl")

model = load_model()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# List of common shortened URL services
SHORTENED_DOMAINS = ["qrco.de", "bit.ly", "goo.gl", "t.co", "tinyurl.com"]

# Function to check if a URL is shortened
def is_shortened_url(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return any(shortened_domain in domain for shortened_domain in SHORTENED_DOMAINS)

# Function to resolve shortened URL
def resolve_shortened_url(shortened_url):
    try:
        response = requests.get(shortened_url, allow_redirects=True)
        return response.url  # Returns the resolved URL
    except requests.exceptions.RequestException as e:
        print(f"Error resolving shortened URL: {e}")
        return None

# Function to extract URL from QR code
def extract_url_from_qr(image_path):
    image = Image.open(image_path)
    decoded_objects = decode(image)
    
    if decoded_objects:
        url = decoded_objects[0].data.decode("utf-8")  # Extract first QR code URL
        print(f"Extracted URL from QR: {url}")
        return url
    return None

# Function to extract text from an image using OCR
def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    extracted_text = pytesseract.image_to_string(processed)
    return extracted_text.strip()

# Function to convert URL into numeric features
def extract_features(url):
    """
    Convert URL into features. This should match the feature extraction 
    process used when training the model.
    """
    parsed_url = urlparse(url)
    features = [
        len(url),                      # URL length
        len(parsed_url.netloc),        # Domain length
        url.count('/'),                # Count of '/'
        url.count('.'),                # Count of '.'
        url.count('-'),                # Count of '-'
        1 if is_shortened_url(url) else 0  # 1 if shortened, else 0
    ]
    return features

# Function to generate hash of a QR code
def get_qr_hash(image_path):
    with open(image_path, "rb") as img_file:
        image_data = img_file.read()
        return hashlib.sha256(image_data).hexdigest()

# Function to check if a QR code is tampered
def is_qr_tampered(image_path):
    new_hash = get_qr_hash(image_path)
    
    if not os.path.exists("original_qr_hash.txt"):
        return None  # No reference QR hash available
    
    with open("original_qr_hash.txt", "r") as file:
        original_hash = file.read().strip()
    
    return new_hash != original_hash  # True if tampered, False if original

@app.route('/')
def home():
    return jsonify({"msg": "Welcome to the Hospital URL Prediction and OCR API!"})

@app.route('/predict', methods=['POST'])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    filepath = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(filepath)
    print(f"Image saved at: {filepath}")

    try:
        # Step 1: Check for QR tampering
        tampered = is_qr_tampered(filepath)
        if tampered is None:
            return jsonify({"error": "Original QR hash not found. Cannot verify tampering."}), 400
        elif tampered:
            return jsonify({"error": "QR Code has been tampered!"}), 400

        # Step 2: Extract URL from QR code
        url = extract_url_from_qr(filepath)
        if not url:
            return jsonify({"error": "No QR code detected or unable to extract URL"}), 400

        # Step 3: Resolve shortened URL if necessary
        resolved_url = None
        if is_shortened_url(url):
            resolved_url = resolve_shortened_url(url)
            if resolved_url:
                print(f"Resolved URL: {resolved_url}")
                url = resolved_url

        # Step 4: Convert URL to numeric features
        url_features = extract_features(url)
        url_features = np.array(url_features).reshape(1, -1)

        # Step 5: Predict using the model
        result = model.predict(url_features)
        print(f"Model Prediction: {result}")  # Debug log

        return jsonify({"prediction": str(result[0]), "resolved_url": resolved_url or url, "tampered": False}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to process request: {str(e)}"}), 400
    
@app.route('/extract_text', methods=['POST'])
def extract_text():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    filepath = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(filepath)

    try:
        extracted_text = extract_text_from_image(filepath)
        return jsonify({"extracted_text": extracted_text}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to extract text: {str(e)}"}), 400

@app.route('/generate-hash', methods=['POST'])
def generate_qr_hash():
    """API to generate and store a hash of the original QR code."""
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    filepath = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(filepath)

    hash_value = get_qr_hash(filepath)

    # Save the hash as a reference for tampering detection
    with open("original_qr_hash.txt", "w") as file:
        file.write(hash_value)

    return jsonify({"message": "Original QR hash saved successfully!", "hash": hash_value})

if __name__ == "__main__":
    app.run(debug=True)