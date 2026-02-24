import azure.functions as func
import json
import logging

from ai_extractor import extract_entities
from rom_engine import generate_rom
from database import save_estimate

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="generate-rom", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def generate_rom_api(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing generate-rom request')
    
    try:
        # Parse request body
        try:
            body = req.get_json()
        except ValueError:
            return func.HttpResponse(
                json.dumps({"error": "Invalid JSON in request body"}),
                mimetype="application/json",
                status_code=400
            )
        
        rfp_text = body.get("rfp_text")

        if not rfp_text:
            return func.HttpResponse(
                json.dumps({"error": "rfp_text is required"}),
                mimetype="application/json",
                status_code=400
            )

        logging.info(f"Processing RFP text: {rfp_text[:100]}...")

        # Step 1: AI Extraction
        try:
            extracted = extract_entities(rfp_text)
            logging.info(f"Extracted data: {extracted}")
        except Exception as e:
            logging.error(f"AI extraction failed: {e}")
            return func.HttpResponse(
                json.dumps({"error": f"AI extraction failed: {str(e)}"}),
                mimetype="application/json",
                status_code=500
            )

        # Step 2: Example rate card
        rate_card = {
            "Program Manager": 120,
            "Developer": 100,
            "Architect": 150
        }

        # Step 3: ROM Calculation
        try:
            rom_result = generate_rom(extracted, rate_card)
            logging.info(f"ROM result: {rom_result}")
        except Exception as e:
            logging.error(f"ROM calculation failed: {e}")
            return func.HttpResponse(
                json.dumps({"error": f"ROM calculation failed: {str(e)}"}),
                mimetype="application/json",
                status_code=500
            )

        result = {
            "extracted_data": extracted,
            "rom_result": rom_result
        }

        # Step 4: Save (non-blocking)
        try:
            save_estimate(result)
        except Exception as e:
            logging.warning(f"Failed to save estimate: {e}")
            # Continue even if save fails

        return func.HttpResponse(
            json.dumps(result, indent=2),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return func.HttpResponse(
            json.dumps({"error": f"Internal server error: {str(e)}"}),
            mimetype="application/json",
            status_code=500
        )