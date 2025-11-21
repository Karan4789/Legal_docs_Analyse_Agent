# Legal Document Analysis Agent

An AI-powered legislative document analysis tool built with **FastAPI**, **LangChain**, and **Google Gemini 2.5 Flash**.  
This application ingests PDF files, extracts text, summarizes the content, identifies key legal sections, and validates the document against specific legislative drafting rules.

---

## 🚀 Features

- **PDF Ingestion**: Upload and parse legislative PDF documents using PyMuPDF.
- **AI-Powered Summarization**: Generates concise bullet-point summaries.
- **Section Extraction**: Automatically extracts Definitions, Eligibility, Payments, Penalties, Responsibilities, and more.
- **Rule Compliance Checks**: Evaluates documents against 6 legal drafting rules and returns Pass/Fail with evidence.
- **Dual Interface**:
  - **FastAPI Backend** for processing
  - **Streamlit Frontend** for a user-friendly UI

---

## 🏛️ Architecture

The project uses a **Client–Server Architecture**:

### **Server – FastAPI Backend**
- Receives PDF files via API  
- Extracts text using PyMuPDF  
- Performs LLM-based processing (Gemini 2.0 Flash via LangChain)  
- Returns structured JSON responses  

### **Client – Streamlit Frontend**
- Allows users to upload PDFs  
- Sends requests to the FastAPI server  
- Displays summaries, extracted sections, and rule-check results  

### **Why Client–Server?**
- Clear separation of concerns  
- The backend can scale independently  
- Any number of future clients (mobile, desktop, chatbots) can reuse the same backend  
- More secure & modular architecture  

---

## 🛠️ Tech Stack

- **Language**: Python 3.12+
- **LLM Framework**: LangChain (`langchain-google-genai`)
- **Model**: Google Gemini 2.0 Flash (via Google AI Studio)
- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **PDF Processing**: PyMuPDF (`fitz`)

---

## 📂 Project Structure

```
universal-credit-agent/
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI entry point and endpoints
│   ├── llm_utils.py        # AI logic: Summaries, Extraction, Rule Checks
│   ├── pdf_processing.py   # PDF text extraction logic
│   └── config.py           # Configuration settings
├── .env                    # Environment variables
├── requirements.txt
├── README.md
└── app_ui.py               # Streamlit UI
```

---

## ⚙️ How It Works

The application consists of two independent components:

### 1. **FastAPI Backend**
- Exposes a `/upload-pdf/` endpoint  
- Extracts text from PDF  
- Sends text to Gemini for summarization, extraction, and rule validation  

### 2. **Streamlit Frontend**
- Uploads PDF  
- Calls the backend  
- Displays results in a friendly UI  

---

## 🧰 Getting Started

### 1. Prerequisites
- Python **3.12+**
- Google API Key for **Gemini**

---

## 🔧 Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd universal-credit-agent
```

Create a virtual environment:

```bash
uv venv
```

Activate it:

**Windows**
```bash
.venv\Scripts\activate
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
uv sync
```

---

## 🔐 Configuration

Create a `.env` file:

```env
GOOGLE_API_KEY="your_google_api_key_here"
```

---

## ▶️ Running the Application

### **Terminal 1 — Backend**
```bash
uvicorn app.main:app --reload
```

### **Terminal 2 — Frontend**
```bash
streamlit run app_ui.py
```

---

## 📤 API Response Structure

```json
{
  "summary": "...",
  "sections": {
    "Definitions": "...",
    "Eligibility": "...",
    "Payments": "..."
  },
  "rule_checks": [
    {
      "rule": "Act must define key terms",
      "status": "pass",
      "evidence": "Section 1 defines 'Universal Credit'...",
      "confidence": 95
    }
  ]
}
```

