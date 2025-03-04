# Document-Extraction-using-LLM

Operations-based use cases involving document extraction in Python with LLMs (Large Language Models) are useful in various domains, including banking, financial crime compliance, legal document processing, and customer support. Given your expertise in financial crime and AI, here are some relevant use cases:

# Financial Crime Compliance (FCC) - KYC & AML Document Extraction
Use Case: Automate the extraction of key details from customer-submitted documents (e.g., passports, utility bills, bank statements) for Know Your Customer (KYC) and Anti-Money Laundering (AML) compliance.
LLM Application: Use LLMs and OCR (e.g., Tesseract, AWS Textract, Google Vision API) to extract and validate key fields like name, address, date of birth, and document validity.

# Step-by-Step KYC Process

# 1️⃣ Customer Onboarding Initiation
 • The customer begins the process by submitting an application.
 • The customer provides necessary identity and address verification documents.
 • For corporate accounts, the customer submits business registration details and Ultimate Beneficial Owner (UBO) information.

# 2️⃣ Document Collection & Verification

✅ For Individuals:
 • Identity Proof: Passport, Driving License, UK Biometric Residence Permit.
 • Address Proof: Utility Bill, Bank Statement, Council Tax Bill (issued within the last 3 months).

✅ For Businesses:
 • Company Incorporation Certificate.
 • UBO Verification.
 • Financial Statements (if required).

# 3️⃣ Identity Verification
 • Automated Checks: AI-driven identity verification, OCR scanning, and biometric face matching (where applicable).
 • Manual Review: In case of discrepancies or issues, further verification may be necessary.

# 4️⃣ Screening & Due Diligence

All applicants undergo thorough checks:
 • Sanctions Screening: Cross-checking with global sanctions lists, including the UK Sanctions List (OFSI), UN, EU, and others.
 • PEP (Politically Exposed Person) Check: Identifying individuals holding high-risk political positions.
 • Adverse Media Screening: Searching for negative media reports linked to financial crimes or illicit activities.
 • Risk Assessment: The applicant is classified into one of three risk levels—Low, Medium, or High.

# 5️⃣ Risk-Based Decisioning
 • Low-Risk: Auto-approval with standard due diligence (SDD).
 • Medium-Risk: Enhanced due diligence (EDD), which may include additional document verification.
 • High-Risk: Comprehensive review with senior compliance approval before making a decision.

# 6️⃣ Customer Approval & Account Activation
 • Approved: The customer is successfully onboarded, and their account is activated.
 • Rejected: The customer is notified of the rejection, with clear reasons provided, in accordance with GDPR and FCA fairness principles.

# 7️⃣ Ongoing Monitoring & Periodic Review
 • Continuous Transaction Monitoring: Ongoing monitoring to detect any unusual activity or patterns in transactions.
 • Periodic KYC Updates: Regular updates based on the customer’s risk profile (e.g., high-risk customers are reviewed annually).
 • Suspicious Activity Reports (SARs): Filed with the National Crime Agency (NCA) if suspicious activity is detected.

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


# Tesseract OCR: Overview & Usage
Tesseract OCR (Optical Character Recognition) is an open-source engine developed by Google for extracting text from images and scanned documents.

# Key Features
✅ Supports multiple languages

✅ Works with printed text, not handwritten

✅ Handles image preprocessing for better accuracy

✅ Can extract text from various formats (JPG, PNG, TIFF, PDF)


# OpenAI chat.completions API
This API is used for chat-based AI responses, like using GPT-4 for document processing, risk scoring, or summarization.

# How It Works
Takes input messages (like a conversation)
Processes with an LLM (GPT-4)
Returns AI-generated output (text-based response)

# Snippet

client = openai.OpenAI(api_key="your_openai_api_key")
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is financial crime?"}
    ]
)

# Explanation
"role": "system" → Defines AI behavior

"role": "user" → User's input message

Model → Supports "gpt-4", "gpt-3.5-turbo", etc.

Output → AI-generated response (response.choices[0].message.content)


# Features of the Pipeline

✅ Extracts text from PDFs & images using Tesseract OCR

✅ Identifies key fields (Name, DOB, Address, Document Type) using Regex

✅ Validates extracted data with GPT (LLM-based validation)

✅ Computes a risk score based on missing fields & document inconsistencies

✅ Stores the results in a structured Pandas DataFrame


# Next Steps
1. Store in a database (MongoDB/PostgreSQL)
2. Add Face Matching with OpenCV
3. Integrate Real-time AML Checks

# Why Use LLM in This Pipeline?
The OCR component (Tesseract) extracts raw text from scanned KYC documents, but it has limitations:

1. OCR makes errors (e.g., misreading letters/numbers).
2. Extracted text is unstructured (no context or validation).
3. Regex-based extraction only finds predefined patterns and misses variations in documents.

LLMs (like GPT-4) enhance the pipeline by: 

✅ Validating the extracted information (detecting inconsistencies or formatting issues).

✅ Handling variations in KYC documents across different banks and regions.

✅ Detecting potential fraud indicators (e.g., invalid document numbers, suspicious addresses).

✅ Providing intelligent risk assessment by analyzing extracted data holistically.

✅ Summarizing & structuring the extracted data to make it easier for compliance teams.

# Key Use Casses of LLM in KYC and AML

![image](https://github.com/user-attachments/assets/25499889-ca96-445e-b18f-113d4ac6a103)

# Where LLM is Most Useful

1. Complex KYC Data Extraction
Handles variations in document layouts.
Extracts structured data intelligently.

2. Fraud Detection & Risk Analysis
Identifies fake names, mismatched DOBs, or altered documents.
Flags high-risk customers for manual review.

3. Data Standardization & Cleansing
Converts extracted text into standardized formats.
Example: Converts "123 Bnk St, Tornto, Can." → "123 Bank Street, Toronto, Canada".

4. Intelligent Risk Scoring
Detects unusual addresses (e.g., "000 Fake Street").
Flags high-risk individuals (e.g., PEPs, blacklisted entities).


# When NOT to Use LLM

1. If Speed is a Priority
LLMs take longer than simple regex-based extraction.
Use LLM only for validation, not for every document.

2. If the Task is Simple (Fixed Templates)
If the document format never changes, regex is faster.

3. If Cost is an Issue
OpenAI API calls cost money.
Use local models (Llama, Falcon) if cost is a concern.
