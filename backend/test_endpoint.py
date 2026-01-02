"""
Test the emotion analysis endpoint directly to see the actual error
"""
import requests
import base64
import cv2
import numpy as np

# Create a simple test image
test_img = np.zeros((480, 640, 3), dtype=np.uint8)
test_img[:] = [100, 150, 200]  # Fill with color

# Encode to base64 (as JPEG)
_, buffer = cv2.imencode('.jpg', test_img)
img_base64 = base64.b64encode(buffer).decode('utf-8')

# Send request
url = "http://localhost:8000/api/emotion/analyze-base64"
payload = {"image": img_base64}

print("Sending request to emotion endpoint...")
try:
    response = requests.post(url, json=payload)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code != 200:
        print(f"\nERROR DETAILS:")
        print(response.json())
except Exception as e:
    print(f"Request failed: {e}")
