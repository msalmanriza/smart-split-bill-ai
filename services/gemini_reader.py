from google import genai
from dotenv import load_dotenv
from PIL import Image
import json
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def extract_receipt(image_path):

    image = Image.open(image_path)

    prompt = """
    Extract receipt information.

    Return valid JSON only.

    {
        "items":[
            {
                "name":"",
                "quantity":1,
                "unit_price":0,
                "total_price":0
            }
        ],
        "subtotal":0,
        "additional_charges":[
            {
                "name":"",
                "amount":0
            }
        ],
        "total_bill":0
    }

    Do not explain.
    Do not use markdown.
    """

    import time

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    prompt,
                    image
                ]
            )

            text = response.text.strip()

            text = text.replace(
                "```json",
                ""
            ).replace(
                "```",
                ""
            )

            return json.loads(text)

        except Exception as e:

            print(
                f"GEMINI RETRY {attempt + 1}:",
                str(e)
            )

            time.sleep(3)

    return {
        "items": [
            {
                "name": "Extraction Failed",
                "quantity": 1,
                "unit_price": 0,
                "total_price": 0
            }
        ],
        "subtotal": 0,
        "additional_charges": [],
        "total_bill": 0
    }