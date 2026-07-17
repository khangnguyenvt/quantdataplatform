import json
import os
from google import genai
from app.config import settings

# Top ~20 pharma/biotech tickers for fast lookup
COMMON_TICKERS = {
    "pfizer inc.": "PFE",
    "pfizer": "PFE",
    "moderna, inc.": "MRNA",
    "moderna": "MRNA",
    "eli lilly and company": "LLY",
    "eli lilly": "LLY",
    "johnson & johnson": "JNJ",
    "j&j": "JNJ",
    "merck & co., inc.": "MRK",
    "merck": "MRK",
    "astrazeneca": "AZN",
    "novartis": "NVS",
    "roche": "RHHBY",
    "sanofi": "SNY",
    "bristol-myers squibb": "BMY",
    "gilead sciences": "GILD",
    "amgen": "AMGN",
    "abbvie": "ABBV",
    "novo nordisk": "NVO",
    "glaxosmithkline": "GSK",
    "gsk plc": "GSK",
    "takeda": "TAK",
    "regeneron": "REGN",
    "biogen": "BIIB",
    "vertex pharmaceuticals": "VRTX"
}

CACHE_FILE = "ticker_cache.json"

class EntityResolver:
    def __init__(self):
        self.cache = {}
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                self.cache = json.load(f)
                
        if settings.gemini_api_key:
            self.client = genai.Client(api_key=settings.gemini_api_key)
        else:
            self.client = None

    def _save_cache(self):
        with open(CACHE_FILE, "w") as f:
            json.dump(self.cache, f, indent=2)

    def resolve_ticker(self, company_name: str) -> str | None:
        if not company_name:
            return None
            
        name_lower = company_name.lower().strip()
        
        # 1. Check hardcoded common list
        if name_lower in COMMON_TICKERS:
            return COMMON_TICKERS[name_lower]
            
        # 2. Check local cache
        if name_lower in self.cache:
            ticker = self.cache[name_lower]
            return ticker if ticker != "NONE" else None
            
        # 3. Fallback to Gemini LLM
        if not self.client:
            return None
            
        try:
            prompt = f"What is the stock ticker symbol for the company '{company_name}'? If it is a publicly traded company on a major exchange, reply with ONLY the ticker symbol (like 'AAPL' or 'PFE'). If it is a university, government agency, private company, or not publicly traded, reply with the exact word 'NONE'."
            
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            result = response.text.strip().upper()
            
            # Clean up the output in case it answered verbose
            if len(result) > 10 and "NONE" not in result:
                result = "NONE" # Fallback if it didn't follow instructions
                
            self.cache[name_lower] = result
            self._save_cache()
            
            return result if result != "NONE" else None
            
        except Exception as e:
            print(f"Error resolving ticker for {company_name}: {e}")
            return None

resolver = EntityResolver()
