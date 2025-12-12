import pdfplumber
import re
import json
import os
from openai import OpenAI
from app.services.nlpExtraction import NplEngine
from app.config import get_settings
# from app.services.llm import extract_with_llm

settings = get_settings()

# os.getenv("OPENAI_settings.AI_SECRET_KEY")
client = OpenAI(api_key=settings.AI_SECRET_KEY) if settings.AI_SECRET_KEY else None

def extract_raw_text(pdf_path):
    """Extracts raw text from a PDF file using pdfplumber."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            raw_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    raw_text += text + "\n"
        return raw_text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

# def extract_receipt_metadata(text):
    """Extracts metadata from receipt text using Regex."""
    metadata = {}

    # Amount
    # Matches: Total: 1,200.00, Amount: 500, etc.
    amount_match = re.search(r"(Total|Amount|Grand Total|Paid)[\s:₹]*([0-9,]+\.\d{2}|[0-9,]+)", text, re.I)
    metadata["amount"] = amount_match.group(2).replace(",", "") if amount_match else None
    
    # Date
    # Matches: 12/01/2025, 12-01-2025, 12.01.2025
    date_match = re.search(r"(Date|Dt)[\s:.-]*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})", text, re.I)
    metadata["date"] = date_match.group(2) if date_match else None

    # GST
    # Matches: GST: 29ABCDE..., GSTIN: ...
    gst_match = re.search(r"(GST|CGST|SGST|IGST|GSTIN)[\s:₹]*([0-9A-Z]{15})", text, re.I)
    metadata["gst"] = gst_match.group(2) if gst_match else None

    # Vendor name (Heuristic: first non-empty line)
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    metadata["vendor"] = lines[0] if lines else None
    
    # Category (Heuristic: keyword search)
    text_lower = text.lower()
    if any(x in text_lower for x in ["uber", "ola", "flight", "ticket", "travel"]):
        metadata["category"] = "Travel"
    elif any(x in text_lower for x in ["hotel", "stay", "room"]):
        metadata["category"] = "Hotel"
    elif any(x in text_lower for x in ["food", "restaurant", "meal", "dinner", "lunch"]):
        metadata["category"] = "Food"
    else:
        metadata["category"] = "Others"

    return metadata

def refine_with_llm(raw_text, metadata):
    """Refines extracted data using OpenAI's LLM."""
    if not client:
        print("OpenAI client not initialized, skipping LLM refinement.")
        return metadata

    prompt = f"""
    You are an expert data extraction assistant. Extract the following fields from the receipt text below.
    Return ONLY a JSON object with these keys: "amount" (float), "date" (YYYY-MM-DD), "vendor" (string), "gst" (string), "category" (Travel, Food, Hotel, Others), "purpose" (string, infer from context).
    
    Use the provided metadata as a starting point but correct it if the text suggests otherwise.
    
    Metadata: {json.dumps(metadata)}
    
    Receipt Text:
    {raw_text[:2000]} # Truncate to avoid token limits if necessary
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Using a cost-effective model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts structured data from receipts."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"LLM refinement failed: {e}")
        return metadata


def extract_with_llm(required_fields, extracted_fields_json):
    """
    required_fields: ["vendor", "amount", "date", ...]
    extracted_fields_json: exact NLP extracted values (no raw text)
    """

    prompt = f"""
You are an AI extraction engine. You will receive:
1. extracted_fields: list of objects containing label and noisy values.
2. required_fields: list of labels to extract.

YOUR TASK:
1. Match required_field with extracted_fields using CASE-INSENSITIVE comparison.
2. Analyse ALL extracted values for each label.
3. Extract **only the clean correct substring**.
4. Remove extra words, irrelevant trailing text, noise.
5. If no valid value exists -> return null.

CLEANING RULES:
• Extract ONLY correct email/date/number/name/policy number etc.
• If text contains multiple fields, keep only part belonging to the label.
• Do NOT return noisy values.
• Confidence = 1 when extraction is accurate.

STRICT OUTPUT FORMAT (NO allValue section):
[
  {{
    "label": "",
    "value": "",
    "confidence": 0.0,
    "reason": ""
  }}
]

extracted_fields:
{extracted_fields_json}

required_fields:
{required_fields}
"""

    # Call ChatGPT
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        max_output_tokens=1500
    )

    # Extract LLM output
    llm_output = response.output_text
    print("LLM Output:", llm_output)  # Debug print  
    # Parse JSON safely
    json_start = llm_output.find("[")
    json_end = llm_output.rfind("]") + 1
    cleaned = llm_output[json_start:json_end]

    return json.loads(cleaned)

def receipt_to_json(pdf_path):
    """Orchestrates the extraction process."""
    raw_text = extract_raw_text(pdf_path)
    print("Raw Text Extracted:", raw_text)  # Print first 500 chars for debugging 
    # metadata = extract_receipt_metadata(raw_text)

    keyswords = ["vendor", "amount", "date", "gst", "category","description"]
    extractor = NplEngine(keyswords)
    print("Extractor:", extractor)
    metadata = extractor.extract(raw_text)
    print("Initial Metadata:", metadata)
    # Refine with LLM
    
    extract_w = extract_with_llm(keyswords,json.dumps(metadata))
    print("Refined Data from LLM:", extract_w)
    
    return {
        "raw_text": raw_text,
        "extracted_data": extract_w
    }
