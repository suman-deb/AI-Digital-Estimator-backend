import os
import json
from openai import AzureOpenAI

def get_openai_client():
    return AzureOpenAI(
        api_key=os.environ["AOAI_KEY"],
        api_version="2024-02-15-preview",
        azure_endpoint=os.environ["AOAI_ENDPOINT"]
    )

def extract_entities(text):
    client = get_openai_client()

    prompt = f"""
You are an AI estimation assistant.

Extract structured estimation parameters from this opportunity brief:

Return ONLY valid JSON with these fields:
- service_categories (array of strings)
- estimated_users (number)
- data_volume_tb (number)
- timeline_months (number)
- complexity (Low/Medium/High)
- migration_scope (string)
- testing_scope (string)

Opportunity Brief:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini-estimator",
        messages=[
            {"role": "system", "content": "You extract structured estimation parameters."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise Exception("AI returned invalid JSON")