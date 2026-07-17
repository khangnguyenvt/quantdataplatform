from google import genai
from app.config import settings

PROMPT_TEMPLATE = """
You are an expert PostgreSQL database analyst for a quantitative hedge fund. 
Your job is to translate a user's natural language question into a valid SQL query.

The database has a single table called `events`:
Table `events`:
- id (UUID)
- event_type (VARCHAR)
- source (VARCHAR)
- entity_name (VARCHAR)
- ticker (VARCHAR)
- sector (VARCHAR)
- published_at (TIMESTAMP WITH TIME ZONE) - When the data became known
- content_date (TIMESTAMP WITH TIME ZONE) - The date the data references
- headline (TEXT)
- structured_fields (JSONB) - Vertical-specific data
- raw_text (TEXT)
- ai_signals (JSONB)

The structured_fields column contains different fields depending on event_type:
For trial events: nct_id, sponsor, phase, status, previous_status, indication, enrollment_actual, enrollment_planned, primary_completion_date, study_type
For patent events: patent_id, patent_title, application_date, grant_date, assignee, patent_type, technology_clusters (array), cpc_codes (array)
For stress_test_result events: bank_name, test_year, test_type (DFAST/CCAR), scenario_type, pre_stress_cet1, post_stress_cet1, stress_capital_buffer, regulatory_minimum_cet1, excess_capital, total_losses_bn, loss_rates (nested JSON with keys: first_lien_mortgages, junior_liens_helocs, commercial_real_estate, credit_cards, commercial_industrial, other_consumer)

Rules:
1. Generate ONLY SELECT statements. Never generate INSERT, UPDATE, DELETE, DROP, or any DDL.
2. Query JSONB fields using PostgreSQL syntax: `structured_fields->>'status'` or `(structured_fields->>'enrollment_actual')::int`.
3. If the user asks for a specific company, try to filter by `ticker` if you know it, or `entity_name ILIKE '%name%'`.
4. Return ONLY the raw SQL query. Do not wrap it in markdown code blocks like ```sql ... ```. No preamble or explanation.
5. Limit results to 50 unless specified otherwise.

Question: {question}
"""

class SQLTranslator:
    def __init__(self):
        if settings.gemini_api_key:
            self.client = genai.Client(api_key=settings.gemini_api_key)
        else:
            self.client = None

    def translate_to_sql(self, question: str) -> str:
        if not self.client:
            return "SELECT headline, published_at FROM events ORDER BY published_at DESC LIMIT 10;"
            
        try:
            prompt = PROMPT_TEMPLATE.format(question=question)
            
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            sql = response.text.strip()
            
            # Remove markdown formatting if the model ignored the instruction
            if sql.startswith("```sql"):
                sql = sql[6:]
            elif sql.startswith("```"):
                sql = sql[3:]
                
            if sql.endswith("```"):
                sql = sql[:-3]
                
            sql = sql.strip()
            return sql
            
        except Exception as e:
            print(f"Error translating SQL: {e}")
            return "SELECT headline, published_at FROM events ORDER BY published_at DESC LIMIT 10;"

sql_translator = SQLTranslator()
