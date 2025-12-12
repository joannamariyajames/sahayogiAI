# ocr_service.py

import pytesseract
from PIL import Image
from typing import List, Dict, Union


def extract_text_from_image(image_file: Union[str, "BytesIO"]) -> str:
    """
    Accepts a file path or a file-like object (like Streamlit's UploadedFile).
    Returns raw text extracted by Tesseract.
    """
    img = Image.open(image_file)
    text = pytesseract.image_to_string(img)
    return text


def parse_bill_text(text: str) -> List[Dict]:
    """
    Naive parser:
    Assumes each line is something like:
        Sugar 1kg 50
        Oil 1L 120

    Last token = amount, everything before = item name.

    Returns list of:
        {
         "item": str,
         "amount": float,
         "customer_name": "Walk-in"
        }
    """
    lines = text.splitlines()
    items = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        # Last part is hopefully amount
        try:
            amount = float(parts[-1].replace("₹", "").replace(",", ""))
        except ValueError:
            continue

        item_name = " ".join(parts[:-1]).strip()
        if not item_name:
            continue

        items.append({
            "item": item_name,
            "amount": amount,
            "customer_name": "Walk-in"
        })

    return items
