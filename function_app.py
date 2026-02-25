import azure.functions as func
import json
import logging
from ai_extractor import extract_entities
from rom_engine import generate_rom
from database import save_estimate

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="generate_rom_api", methods=["GET", "POST"], auth_level=func.AuthLevel.ANONYMOUS)
def generate_rom_api(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing generate_rom_api request')
    
    # CORS Headers
    headers = {
        'Access-Control-Allow-Origin': 'https://zealous-bush-08e66e603.4.azurestaticapps.net',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # Handle OPTIONS preflight request
    if req.method == "OPTIONS":
        return func.HttpResponse(
            status_code=200,
            headers=headers
        )
    
    # Handle GET request
    if req.method == "GET":
        return func.HttpResponse(
            json.dumps({
                "message": "ROM Estimator API",
                "usage": "Send POST request with JSON body",
                "example": {"rfp_text": "We need 3 developers for 6 months"}
            }, indent=2),
            mimetype="application/json",
            status_code=200,
            headers=headers
        )
    
    # Handle POST request
    try:
        try:
            body = req.get_json()
        except ValueError:
            return func.HttpResponse(
                json.dumps({"error": "Invalid JSON"}),
                mimetype="application/json",
                status_code=400,
                headers=headers
            )
        
        rfp_text = body.get("rfp_text")
        if not rfp_text:
            return func.HttpResponse(
                json.dumps({"error": "rfp_text is required"}),
                mimetype="application/json",
                status_code=400,
                headers=headers
            )
        
        logging.info(f"Processing: {rfp_text[:100]}...")
        
        # AI Extraction
        try:
            extracted = extract_entities(rfp_text)
            logging.info(f"Extracted: {extracted}")
        except Exception as e:
            logging.error(f"AI extraction failed: {e}")
            return func.HttpResponse(
                json.dumps({"error": f"AI extraction failed: {str(e)}"}),
                mimetype="application/json",
                status_code=500,
                headers=headers
            )
        
        # Rate card
        rate_card = {
            "Program Manager": 120,
            "Developer": 100,
            "Architect": 150
        }
        
        # ROM Calculation
        try:
            rom_result = generate_rom(extracted, rate_card)
            logging.info(f"ROM: {rom_result}")
        except Exception as e:
            logging.error(f"ROM failed: {e}")
            return func.HttpResponse(
                json.dumps({"error": f"ROM calculation failed: {str(e)}"}),
                mimetype="application/json",
                status_code=500,
                headers=headers
            )
        
        result = {
            "extracted_data": extracted,
            "rom_result": rom_result
        }
        
        # Save
        try:
            save_estimate(result)
        except Exception as e:
            logging.warning(f"Save failed: {e}")
        
        return func.HttpResponse(
            json.dumps(result, indent=2),
            mimetype="application/json",
            status_code=200,
            headers=headers
        )
        
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500,
            headers=headers
        )