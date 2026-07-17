from google import genai
from app.config import settings

class Summarizer:
    def __init__(self):
        if settings.gemini_api_key:
            self.client = genai.Client(api_key=settings.gemini_api_key)
        else:
            self.client = None

    def generate_clinical_headline(self, title: str, status: str, phase: str, condition: str, sponsor: str) -> str:
        if not self.client:
            return f"{sponsor} {phase} trial for {condition} is now {status}"
            
        try:
            prompt = f"""
            Write a concise, 1-line professional headline for a quant trading dashboard about this clinical trial update.
            Sponsor: {sponsor}
            Condition: {condition}
            Phase: {phase}
            New Status: {status}
            Trial Title: {title}
            
            Examples:
            - Moderna Phase 3 mRNA-1283 COVID booster trial completed enrollment (n=6,000)
            - Pfizer Phase 2 breast cancer study terminated due to efficacy concerns
            - Eli Lilly initiates Phase 1 trial for novel Alzheimer's candidate
            
            Return ONLY the headline, no quotes or intro text.
            """
            
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error generating headline: {e}")
            return f"{sponsor} {phase} trial for {condition} is now {status}"

summarizer = Summarizer()
