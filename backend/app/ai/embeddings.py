from typing import List
from google import genai
from app.config import settings

class EmbeddingsGenerator:
    def __init__(self):
        if settings.gemini_api_key:
            self.client = genai.Client(api_key=settings.gemini_api_key)
        else:
            self.client = None

    def generate_embedding(self, text: str) -> List[float]:
        if not self.client or not text:
            return None
            
        try:
            response = self.client.models.embed_content(
                model='text-embedding-004',
                contents=text,
            )
            return response.embeddings[0].values
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        if not self.client or not texts:
            return [None] * len(texts)
            
        try:
            response = self.client.models.embed_content(
                model='text-embedding-004',
                contents=texts,
            )
            return [emb.values for emb in response.embeddings]
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return [None] * len(texts)

embeddings_gen = EmbeddingsGenerator()
