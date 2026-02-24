
import azure.functions as func
import json

from ai_extractor import extract_entities
from rom_engine import generate_rom
from database import save_estimate

app = func.FunctionApp()

@app.route(route="generate-rom", methods=["POST"])
def generate_rom_api(req: func.HttpRequest) -> func.HttpResponse:

    try:
        body = req.get_json()
        rfp_text = body.get("rfp_text")

        if not rfp_text:
            return func.HttpResponse(
                "rfp_text is required",
                status_code=400
            )

        # Step 1: AI Extraction
        extracted = extract_entities(rfp_text)

        # Step 2: Example rate card
        rate_card = {
            "Program Manager": 120
        }

        # Step 3: ROM Calculation
        rom_result = generate_rom(extracted, rate_card)

        result = {
            "extracted_data": extracted,
            "rom_result": rom_result
        }

        # Step 4: Save
        save_estimate(result)

        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(
            str(e),
            status_code=500
        )