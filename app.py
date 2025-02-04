import os
import pytesseract
import openai
import pdfplumber
import pandas as pd
import re
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image

# Set OpenAI API key (Use environment variable for security)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to preprocess image for better OCR results
def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # Apply thresholding
    return image

# Function to extract text from an image
def extract_text_from_image(image_path):
    processed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed_image)
    return text

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Function to extract key KYC details using regex
def extract_kyc_details(text):
    details = {
        "Name": None,
        "Date of Birth": None,
        "Address": None,
        "Document Type": None
    }

    # Extract Name
    name_match = re.search(r"Name[:\s]+([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)", text)
    if name_match:
        details["Name"] = name_match.group(1)

    # Extract Date of Birth (DOB)
    dob_match = re.search(r"Date of Birth[:\s]+(\d{2}/\d{2}/\d{4}|\d{2}-\d{2}-\d{4})", text)
    if dob_match:
        details["Date of Birth"] = dob_match.group(1)

    # Extract Address
    address_match = re.search(r"Address[:\s]+([\w\s,]+)", text)
    if address_match:
        details["Address"] = address_match.group(1)

    # Identify document type
    if "passport" in text.lower():
        details["Document Type"] = "Passport"
    elif "license" in text.lower():
        details["Document Type"] = "Driver's License"
    else:
        details["Document Type"] = "Unknown"

    return details

# Function to compute risk score based on extracted KYC details
def compute_risk_score(kyc_data):
    risk_score = 0

    # Missing fields increase risk
    missing_fields = sum(1 for key, value in kyc_data.items() if value is None)
    risk_score += missing_fields * 15  # Each missing field adds 15 to the risk

    # Document type risk factor
    if kyc_data["Document Type"] == "Unknown":
        risk_score += 20  # Unknown document increases risk

    # Invalid Date of Birth format
    if kyc_data["Date of Birth"] and not re.match(r"\d{2}/\d{2}/\d{4}|\d{2}-\d{2}-\d{4}", kyc_data["Date of Birth"]):
        risk_score += 10  # Bad DOB format increases risk

    # Short address may indicate fraud
    if kyc_data["Address"] and len(kyc_data["Address"]) < 10:
        risk_score += 10

    # Cap risk score at 100
    risk_score = min(risk_score, 100)

    # Categorize risk level
    risk_level = "Low Risk" if risk_score <= 20 else "Medium Risk" if risk_score <= 50 else "High Risk"
    
    return risk_score, risk_level

# Function to validate KYC details using OpenAI GPT model
def validate_kyc_details(kyc_data):
    prompt = f"""
    Validate the following KYC details extracted from a document:
    - Name: {kyc_data['Name']}
    - Date of Birth: {kyc_data['Date of Birth']}
    - Address: {kyc_data['Address']}
    - Document Type: {kyc_data['Document Type']}

    Check if the details are complete and formatted correctly.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a compliance officer analyzing KYC data."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# Function to process a KYC document
def process_kyc_document(file_path):
    if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
        text = extract_text_from_image(file_path)
    elif file_path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        print("Unsupported file format!")
        return

    print("\nExtracted Text:\n", text)

    kyc_details = extract_kyc_details(text)
    print("\nExtracted KYC Details:", kyc_details)

    # Compute risk score
    risk_score, risk_level = compute_risk_score(kyc_details)
    print(f"\nRisk Score: {risk_score} ({risk_level})")

    # Validate using LLM
    validation_result = validate_kyc_details(kyc_details)
    print("\nValidation & LLM Insights:\n", validation_result)

    # Store results in a DataFrame
    df = pd.DataFrame([{
        "Name": kyc_details["Name"],
        "Date of Birth": kyc_details["Date of Birth"],
        "Address": kyc_details["Address"],
        "Document Type": kyc_details["Document Type"],
        "Risk Score": risk_score,
        "Risk Level": risk_level
    }])

    return df

# Example usage
if __name__ == "__main__":
    file_path = "/Users/rupeshshivsharan/Downloads/Rupesh_passport.pdf"  # Replace with your actual file
    df = process_kyc_document(file_path)
    print("\nFinal Processed Data:\n", df)
