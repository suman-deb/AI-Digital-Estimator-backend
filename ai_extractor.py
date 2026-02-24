import os
import json
from openai import AzureOpenAI

def get_openai_client():
    return AzureOpenAI(
        api_key=os.environ.get("AOAI_KEY"),
        api_version="2024-02-15-preview",
        azure_endpoint=os.environ.get("AOAI_ENDPOINT")
    )

def extract_entities(text):
    try:
        client = get_openai_client()

        prompt = f"""Extract structured estimation parameters from this opportunity brief.

Return ONLY valid JSON with these exact fields:
{{
  "service_categories": ["category1", "category2"],
  "estimated_users": 100,
  "data_volume_tb": 1,
  "timeline_months": 6,
  "complexity": "Medium",
  "migration_scope": "scope description",
  "testing_scope": "testing description"
}}

Opportunity Brief:
{text}

JSON Response:"""

        response = client.chat.completions.create(
            model="gpt-4o-mini-estimator",
            messages=[
                {"role": "system", "content": "You extract structured estimation parameters. Return ONLY valid JSON, no markdown, no explanations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )

        content = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        
        if content.endswith("```"):
            content = content[:-3]
        
        content = content.strip()
        
        # Parse JSON
        extracted_data = json.loads(content)
        
        # Validate required fields
        required_fields = ["timeline_months", "complexity"]
        for field in required_fields:
            if field not in extracted_data:
                extracted_data[field] = 6 if field == "timeline_months" else "Medium"
        
        return extracted_data
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"AI response was: {content}")
        raise Exception(f"AI returned invalid JSON: {str(e)}")
    except KeyError as e:
        raise Exception(f"Missing environment variable: {str(e)}")
    except Exception as e:
        print(f"AI extraction error: {e}")
        raise Exception(f"AI extraction failed: {str(e)}")