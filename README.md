# QR-Based Fake URL Detection System

## Overview
The **QR-Based Fake URL Detection System** is an intelligent tool designed to analyze QR codes, extract URLs, and classify them as either genuine or fake. Using a combination of image processing, feature engineering, and machine learning.

---

## Workflow

1. **User Uploads QR Code Image**  
   - The user uploads a QR code image via a Vite + React-based frontend.

2. **Image Sent to Flask API for Processing**  
   - The uploaded image is sent to a Flask backend for further processing.

3. **QR Code Decoding**  
   - The Flask API extracts the URL from the QR code using libraries like OpenCV and Pyzbar.

4. **URL Analysis**  
   - Checks if the URL is shortened and resolves it if necessary.
   - Extracts URL features (length, keywords, patterns, etc.) through feature engineering.

5. **Prediction**  
   - A machine learning model (XGBoost classifier) predicts whether the URL is real or fake based on extracted features.

6. **Response Generation**  
   - The system sends the prediction result (in JSON format) to the frontend for user feedback.

---

## Features

- **Frontend**:  
  - User-friendly interface for uploading QR code images.
  - Built with Vite and React for fast and interactive performance.

- **Backend**:  
  - Flask-based API for processing images and handling predictions.
  - Image decoding powered by OpenCV and Pyzbar.

- **Machine Learning**:  
  - Utilizes an XGBoost classification model to predict URL authenticity.
  - Feature engineering extracts meaningful patterns for accurate predictions.

- **Short URL Resolution**:  
  - Handles shortened URLs by expanding them before analysis.

- **JSON Response**:  
  - Provides structured and concise feedback to the user.

---

# Technologies Used
---
- Frontend: React, Vite, Tailwind CSS
- Backend: Flask, OpenCV, Pyzbar
- Machine Learning: XGBoost
- Feature Engineering: URL pattern analysis, length detection, and keyword extraction
- Data Exchange: RESTful API with JSON responses
---

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- pipenv (for Python dependencies)

### Backend Setup
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/qr-fake-url-detector.git

2.Navigate to the backend folder
  ```bash
  cd back
```
3.Start the Flask API (Verify to install the dependencies
```bash
   python server.py
```

### Frontend Setup
1.Navigate to the frontend folder & Install dependencies
```bash 
  npm install
```

2.Start the React application
```bash 
  npm run dev
```

# PREVIEW
![Screenshot 2025-02-14 191028](https://github.com/user-attachments/assets/13b0b6a1-75c9-493f-9f93-cd05f20032f0)
# AUTHENTIC CERTIFICATE
![Screenshot 2025-02-14 191049](https://github.com/user-attachments/assets/82c831ba-7c23-484f-9c12-53f5c6a73903)
# FAKE CERTIFICATE
![image](https://github.com/user-attachments/assets/057f7991-0aea-4f15-84d4-150d97583d4a)
