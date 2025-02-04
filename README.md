# Document-Extraction-using-LLM

Operations-based use cases involving document extraction in Python with LLMs (Large Language Models) are useful in various domains, including banking, financial crime compliance, legal document processing, and customer support. Given your expertise in financial crime and AI, here are some relevant use cases:

# Financial Crime Compliance (FCC) - KYC & AML Document Extraction
Use Case: Automate the extraction of key details from customer-submitted documents (e.g., passports, utility bills, bank statements) for Know Your Customer (KYC) and Anti-Money Laundering (AML) compliance.
LLM Application: Use LLMs and OCR (e.g., Tesseract, AWS Textract, Google Vision API) to extract and validate key fields like name, address, date of birth, and document validity.

# Operations Workflow:
1. Receive scanned KYC documents.
2. Extract text using OCR.
3. Use LLMs to categorize and validate extracted data.
4. Compare with the bank’s internal database for verification.

Python implementation for KYC & AML Document Extraction using OCR and LLMs (GPT).

# Key Features of the Code:
OCR Processing (Extract text from scanned KYC documents)
LLM Integration (Validate and classify extracted data)
Data Cleaning & Extraction (Identify key fields: Name, Address, Date of Birth, etc.)
Validation & Risk Analysis (Cross-check extracted data with predefined rules)

# How It Works
Extracts text from scanned images (PNG, JPG, PDF) using Tesseract OCR.
Uses regex to identify and extract Name, Date of Birth, Address, and Document Type.
Sends extracted details to OpenAI’s GPT model for validation and risk assessment.
Outputs structured KYC data and fraud risk score.


# Expected Output: 
Extracted Text:
Name: John Doe
Date of Birth: 15-08-1985
Address: 123 Bank Street, Toronto, Canada
Document: Passport

Extracted KYC Details:
{'Name': 'John Doe', 'Date of Birth': '15-08-1985', 'Address': '123 Bank Street, Toronto, Canada', 'Document Type': 'Passport'}

# future enhancement: 
Adding the Risk Score
Validation & Risk Assessment:
"The extracted KYC details are complete and valid. Risk Score: 10 (Low Risk)."

# Enhanced Risk Scoring Logic
We will define a custom function to calculate a risk score (0-100) based on:

1. Completeness of KYC Data (Missing fields increase risk)
2. Document Type Validation (Unknown document types increase risk)
3. Pattern Anomalies (Incorrectly formatted names, dates, or addresses increase risk)
4. Manual Risk Factors (E.g., flagged addresses, mismatched DOB, unusual names)

# Updated Risk Scoring Mechanism
Factor	                        Penalty
Missing Fields (per field)	    +15
Unknown Document Type	          +20
Invalid DOB Format	            +10
Short Address (<10 chars)	      +10
Max Risk Score	                100

# Risk Categories
0-20 → Low Risk ✅ (Complete, valid KYC)
21-50 → Medium Risk ⚠️ (Some missing data)
51-100 → High Risk 🔴 (Many missing fields, fraud indicators)

