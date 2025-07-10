# 📝 Grant Extractor Pipeline

This is a lightweight, cost-efficient AI pipeline to **automatically extract structured grant information from web pages and PDF documents, and store it into a Google Sheets spreadsheet.**

It uses:
- ✅ **Python** for scraping, PDF parsing, and orchestration
- ✅ **OpenAI GPT-3.5-turbo** for structured data extraction
- ✅ **Google Sheets API** to save results
- ✅ **GitHub Actions** to run daily, totally serverless and free

---

## 🚀 Features
- 🔍 Scrapes grant data from both **HTML web pages** and **PDF files**
- 🤖 Uses an LLM to extract key fields like funder name, amount, deadline, eligibility, and link
- 📝 Appends new data to a Google Sheet
- ⏰ Runs automatically on a schedule via GitHub Actions (daily at 8 AM UTC)
- 💰 Costs near $0/month — only minor OpenAI charges for API calls

---

## ⚙️ How it works
```
[ GitHub Actions ]
       ⬇
[ Python script ]
       ⬇
[ Scrapes HTML & PDFs ]
       ⬇
[ GPT-3.5-turbo extracts JSON ]
       ⬇
[ Appends to Google Sheets ]
```

---

## 📂 Project structure
```
grant_extractor/
│
├── run_pipeline.py       # Main pipeline script
├── requirements.txt      # Python dependencies
├── .env                  # Local testing config (not committed)
│
└── .github/
    └── workflows/
        └── workflow.yml  # GitHub Actions CI/CD scheduler
```

---

## 🚀 Getting started

### ✅ 1. Clone the repository
```bash
git clone https://github.com/your-username/grant_extractor.git
cd grant_extractor
```

### ✅ 2. Set up local environment
Install dependencies:
```bash
pip install -r requirements.txt
```

Create a `.env` file (for local testing only):
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
GOOGLE_CREDS_JSON={"type":"service_account",...}
```
- `GOOGLE_CREDS_JSON` should be the **full service account JSON** on one line.

---

## 🏃 Running locally
```bash
python run_pipeline.py
```

---

## 🚀 Automated runs via GitHub Actions
This repo uses GitHub Actions to:
- Run the pipeline **every day at 8 AM UTC**
- You can also trigger manually under the “Actions” tab.

### 🔐 Set up repository secrets
Go to your GitHub repo:
- Settings → Secrets → Actions → **New repository secret**
    - `OPENAI_API_KEY`: your OpenAI API key
    - `GOOGLE_CREDS_JSON`: full service account JSON string (one line, no breaks)

---

## 🔍 What gets extracted?
For each document (HTML or PDF), the pipeline uses an LLM to extract:
- `funder_name`
- `grant_amount`
- `deadline`
- `eligibility`
- `url`

and appends these as new rows in your Google Sheet.

---

## 🚀 Deployment summary
✅ **No servers required.**  
✅ **Fully automated.**  
✅ **Costs ~$0.20/month depending on usage.**

