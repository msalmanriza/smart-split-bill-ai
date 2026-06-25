import json

def parse_receipt(text):
    try:
        clean = text.strip()
        if clean.startswith("```"):
            clean = clean.split("```")[1]
            if clean.startswith("json"):
                clean = clean[4:]
            clean = clean.strip()

        return json.loads(clean)
    
    except json.JSONDecodeError:
        return {
            "items": [],
            "subtotal": 0,
            "additional_charges": [],
            "total_bill": 0
        }