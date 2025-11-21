import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"
TEMP_PDF_PATH = "./data/"
