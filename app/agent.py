import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load .env variables
load_dotenv()

# Read API key from environment
API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini LLM
# Replace 'gemini-2.0-flash' with 'gemini-2.5-flash' if available to you
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=API_KEY,
    temperature=0.3
)

def summarize_text(text: str) -> str:
    prompt = PromptTemplate.from_template(
        "Summarize this document into 5-10 bullet points:\n{document}"
    )
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"document": text})

def clean_json_string(text: str) -> str:
    """Removes Markdown code formatting from LLM response."""
    cleaned = text.strip()
    # Remove opening code block with or without language specifier
    if cleaned.startswith("```"):
        # Find the first newline to slice off ```json or ```
        newline_index = cleaned.find("\n")
        if newline_index != -1:
            cleaned = cleaned[newline_index+1:]
    # Remove closing code block
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return cleaned.strip()

def extract_sections(text: str, sections: list = None):
    if sections is None:
        sections = ["Definitions", "Obligations", "Responsibilities", "Eligibility", "Payments", "Penalties"]
    
    sections_list = "\n".join([f"- {section}" for section in sections])
    
    prompt = PromptTemplate.from_template(
        "Extract the following sections from the text and return ONLY a valid JSON object. "
        "Do not include Markdown formatting like ```"
        "Sections to extract:\n{sections_list}\n\n"
        "Text:\n{text}"
        "If a section is not present in the text, return 'Not specified' instead of an empty string."
    )
    
    chain = prompt | llm | StrOutputParser()
    response_text = chain.invoke({"sections_list": sections_list, "text": text})
    
    # Clean up potential markdown code blocks if the model ignores the instruction
    cleaned_text = clean_json_string(response_text)
    
    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        return {"error": "Could not parse the response into JSON", "raw_response": response_text}

def apply_rule_checks(text: str):
    rules = [
        "Act must define key terms",
        "Act must specify eligibility criteria",
        "Act must specify responsibilities of the administering authority",
        "Act must include enforcement or penalties",
        "Act must include payment calculation or entitlement structure",
        "Act must include record-keeping or reporting requirements",
    ]
    rules_text = "\n".join([f"{i+1}. {rule}" for i, rule in enumerate(rules)])
    
    prompt = PromptTemplate.from_template(
        "Evaluate the following rules against this legislative text. "
        "For each rule, return a JSON object with keys 'rule', 'status' (pass/fail), "
        "'evidence' (section or supporting text), and 'confidence' (0-100). "
        "Return ONLY a valid JSON array of objects. Do not include Markdown formatting like ```json.\n\n"
        "Rules:\n{rules_text}\n\n"
        "Text:\n{text}"
    )
    
    chain = prompt | llm | StrOutputParser()
    response_text = chain.invoke({"rules_text": rules_text, "text": text})
    
    # Clean up potential markdown code blocks
    cleaned_text = clean_json_string(response_text)
    
    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        return {"error": "Could not parse the response into JSON", "raw_response": response_text}
