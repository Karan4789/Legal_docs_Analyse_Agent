from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from app.pdf_processing import extract_text_from_pdf
from app.agent import summarize_text, extract_sections, apply_rule_checks

app = FastAPI()

# Ensure the data folder exists
TEMP_DIR = "./data"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")

    file_path = os.path.join(TEMP_DIR, file.filename)

    # Save uploaded file locally temporarily
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Extract text
    pdf_text = extract_text_from_pdf(file_path)

    # Summarize
    summary = summarize_text(pdf_text)

    # Extract sections
    sections = extract_sections(pdf_text)

    # Apply rule checks
    rule_check_results = apply_rule_checks(pdf_text)

    # Clean up - Optional: Remove the file after processing
    os.remove(file_path)

    # Return a combined JSON response
    return JSONResponse(content={
        "summary": summary,
        "sections": sections,
        "rule_checks": rule_check_results
    })
