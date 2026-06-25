from transformers import DonutProcessor
from transformers import VisionEncoderDecoderModel
from PIL import Image
import re

processor = DonutProcessor.from_pretrained(
    "naver-clova-ix/donut-base-finetuned-cord-v2"
)

model = VisionEncoderDecoderModel.from_pretrained(
    "naver-clova-ix/donut-base-finetuned-cord-v2"
)

def extract_receipt(image_path):

    image = Image.open(
        image_path
    ).convert("RGB")

    pixel_values = processor(
        image,
        return_tensors="pt"
    ).pixel_values

    outputs = model.generate(
        pixel_values,
        max_length=512
    )

    result = processor.batch_decode(
        outputs,
        skip_special_tokens=True
    )

    raw_text = result[0]

    numbers = re.findall(
        r"\d+[.,]?\d*",
        raw_text
    )

    prices = []
    seen = set()

    for value in numbers:

        try:

            amount = int(
                value.replace(".", "")
                     .replace(",", "")
            )

            if (
                amount >= 1000
                and amount <= 5000000
                and amount not in seen
            ):

                prices.append(amount)
                seen.add(amount)

        except:
            pass

    prices = sorted(
        prices,
        reverse=True
    )

    prices = prices[:5]

    items = []

    for index, price in enumerate(
        prices
    ):

        items.append(
            {
                "name": f"Item {index + 1}",
                "quantity": 1,
                "unit_price": price,
                "total_price": price
            }
        )

    subtotal = sum(
        item["total_price"]
        for item in items
    )

    return {
        "items": items,
        "subtotal": subtotal,
        "additional_charges": [],
        "total_bill": subtotal,
        "raw_text": raw_text
    }