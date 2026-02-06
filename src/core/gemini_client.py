import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("API key not found. Check .env file.")
        
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-3-flash-preview"
        self.system_prompt = (
            "You are an expert Network Security Analyst conducting a vulnerability assessment. "
            "Analyze the following open port data and provide a 1-sentence risk assessment. You will be given exactly the following 3 things: the port number, the service (if it is known), and a banner"
            "Focus on: 1. Potential vulnerabilities. 2. Initial attack vectors. 3. Specific known exploits."
        )
    def gemini_response(self, service, port, banner):
        user_input = f"Port: {port}, Service: {service}, Banner: {banner}"
        
        response = self.client.models.generate_content(
            model=self.model_id,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                temperature=0.2,
            ),
            contents=user_input
        )
        
        return response.text