# ocr_service.py

import pytesseract
from PIL import Image
from typing import List, Dict, Union
from io import BytesIO


def extract_text_from_image(image_file: Union[str, "BytesIO"]) -> str:
    """
    Accepts a file path or a file-like object (like Streamlit's UploadedFile).
    Returns raw text extracted by Tesseract.
    """
    img = Image.open(image_file)
    text = pytesseract.image_to_string(img)
    return text


def parse_bill_text(text: str) -> List[Dict]:
    import re
    items = []

    pattern = r"(.+?)[\s:]+(\d+\.?\d*)$"   # item name + number at end

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        match = re.search(pattern, line)
        if not match:
            continue

        item_name = match.group(1).strip()
        amount = float(match.group(2))

        items.append({
            "item": item_name,
            "amount": amount,
            "customer_name": "Walk-in"
        })

    return items