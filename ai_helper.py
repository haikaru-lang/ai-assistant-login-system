import os
from dotenv import load_dotenv
from google import genai

# Explicitly load .env file from current folder
load_dotenv(override=True)

class AIAssistant:
    def __init__(self):
        # Fetch key from environment
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        # Diagnostic print to help debug in VS Code terminal
        if not self.api_key:
            print("[DEBUG] GEMINI_API_KEY is missing or empty!")
            self.client = None
        else:
            # Clean spaces or hidden quotes
            cleaned_key = self.api_key.strip().strip('"').strip("'")
            print(f"[DEBUG] Loaded Key: {cleaned_key[:5]}... (Length: {len(cleaned_key)})")
            
            # Initialize Client explicitly with API key
            self.client = genai.Client(api_key=cleaned_key)

    def ask(self, prompt: str) -> str:
        if not self.client:
            return "Error: GEMINI_API_KEY not found or invalid. Please check your .env file."
        
        try:
            response = self.client.models.generate_content(
                model='gemini-3.5-flash',
                contents=prompt,
            )
            return response.text
        except Exception as e:
            return f"AI Service Error: {str(e)}"