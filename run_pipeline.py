import os
import json
import requests
from bs4 import BeautifulSoup
import pdfplumber
#import openai
import groq
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# Load .env for local testing
load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")
groq.api_key = os.getenv("GROQ_API_KEY")

# Google Sheets setup
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    json.loads(os.getenv("GOOGLE_CREDS_JSON")), scopes=SCOPES
)
gc = gspread.authorize(creds)
sheet = gc.open("Grants Data").sheet1

# Example sources
SOURCES = [
    {"type": "html", "url": "https://grants.nih.gov/grants/guide/pa-files/PA-20-185.html"}
]

def extract_text_from_html(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup.get_text()

def extract_text_from_pdf(url):
    resp = requests.get(url)
    with open("temp.pdf", "wb") as f:
        f.write(resp.content)
    text = ""
    with pdfplumber.open("temp.pdf") as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_structured_data(text):
    import re

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    prompt = f"""
You are an expert grant extractor. 
Extract the following fields as JSON:
- funder_name
- grant_amount
- deadline
- eligibility
- url
If missing, use null.

Document:
\"\"\"
{text[:4000]}
\"\"\"
"""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-70b-8192",  # or "mixtral-8x7b-32768"
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    print("Groq returned:", content)  # debug print

    # Try to extract JSON block from markdown or text
    match = re.search(r"\{[\s\S]*?\}", content)
    if match:
        json_str = match.group(0)
        return json.loads(json_str)
    else:
        # fallback: return all fields as null
        return {
            "funder_name": None,
            "grant_amount": None,
            "deadline": None,
            "eligibility": None,
            "url": None
        }

def update_sheet(data):
    sheet.append_row([
        data.get("funder_name"),
        data.get("grant_amount"),
        data.get("deadline"),
        data.get("eligibility"),
        data.get("url")
    ])

def run_pipeline():
    for source in SOURCES:
        if source["type"] == "html":
            text = extract_text_from_html(source["url"])
        elif source["type"] == "pdf":
            text = extract_text_from_pdf(source["url"])
        else:
            continue
        data = extract_structured_data(text)
        update_sheet(data)

if __name__ == "__main__":
    run_pipeline()
