import google.generativeai as genai
from django.conf import settings
import sys

# Configure Gemini once
genai.configure(api_key=settings.GEMINI_API_KEY)

def get_gemini_response(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        print("try", file=sys.stderr)
        print(f"response: {response.text}", file=sys.stderr)
        return response.text
    except Exception as e:
        print(f"Error occurred: {e}", file=sys.stderr)
        return f"Error: {str(e)}"
