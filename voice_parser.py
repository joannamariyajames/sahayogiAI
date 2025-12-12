import re

ACTION_CORRECTIONS = {
    "sail": "sale",
    "sell": "sale",
    "cell": "sale",
}

NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "fire": 5,     # whisper mistake
    "for": 4,
}

NAME_CORRECTIONS = {
    "promise": "ramesh",
    "ramish": "ramesh",
    "ramas": "ramesh",
}

def normalize_words(text: str):
    words = text.split()
    fixed = []

    for w in words:
        if w in ACTION_CORRECTIONS:
            fixed.append(ACTION_CORRECTIONS[w])
        elif w in NAME_CORRECTIONS:
            fixed.append(NAME_CORRECTIONS[w])
        elif w in NUMBER_WORDS:
            fixed.append(str(NUMBER_WORDS[w]))
        else:
            fixed.append(w)

    return " ".join(fixed)

def parse_voice_command(text: str):
    """
    Supports:
    - add sale ramesh apples 5
    - sale ramesh apples five
    - add sail ramesh apples fire
    """

    text = normalize_words(text)

    # detect action
    if "sale" in text:
        action = "add_sale"
    elif "udhaar" in text or "loan" in text:
        action = "add_udhaar"
    else:
        return {"error": "Action not found"}

    # extract amount
    amount_match = re.search(r"\b(\d+)\b", text)
    if not amount_match:
        return {"error": "Amount not found"}

    amount = int(amount_match.group(1))

    # remove keywords
    cleaned = re.sub(r"\b(add|sale|udhaar|loan|\d+)\b", "", text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    parts = cleaned.split(" ")

    if len(parts) < 2:
        return {"error": "Customer or item missing"}

    customer_name = parts[0]
    item = " ".join(parts[1:])

    return {
        "action": action,
        "customer_name": customer_name,
        "item": item,
        "amount": amount,
    }