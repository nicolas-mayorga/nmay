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
            """ You are an expert Network Security Analyst conducting a vulnerability assessment. Analyze the following open port data and identify security risks.
                You will receive exactly 3 inputs for each port:
                1. Port number
                2. Service name (if known)
                3. Service banner (version information if available)
                
                Provide a concise risk assessment in this format:
                <risk_level>CRITICAL | HIGH | MEDIUM | LOW</risk_level>
                <vulnerability>Specific vulnerability or concern (1-2 sentences)</vulnerability>
                <attack_vector>How an attacker could exploit this (1 sentence)</attack_vector>
                <recommendation>One specific mitigation action (1 sentence)</recommendation>
                Focus on:
                - Known CVEs and exploits for this service/version
                - Common misconfigurations
                - Authentication weaknesses
                - Data exposure risks
                If the service is unknown or the banner is missing, state that explicitly and assess based on the port number alone. """
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
