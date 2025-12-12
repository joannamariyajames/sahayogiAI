# voice_service.py

import speech_recognition as sr


def transcribe_from_mic(timeout: int = 5) -> str:
    """
    Records audio from default microphone and uses Google Web Speech API to
    transcribe it. Requires internet for the API.

    Used mainly for local terminal testing, not strictly needed in Streamlit.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        audio = r.listen(source, timeout=timeout)

    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        return text
    except Exception as e:
        print("Error:", e)
        return ""


def parse_command(text: str):
    """
    Parse a very simple command language:
      - "add udhaar <customer> <item words...> <amount>"
      - "repayment <customer> <amount>"

    Returns a dict describing the action.
    """
    text = text.lower().strip()
    if not text:
        return {"action": "unknown"}

    words = text.split()
    if len(words) < 3:
        return {"action": "unknown"}

    # add udhaar Ramesh sugar 50
    if words[0] == "add" and words[1] == "udhaar":
        # words[2] = customer
        customer = words[2]
        try:
            amount = float(words[-1])
        except ValueError:
            return {"action": "unknown"}

        # item is everything between words[3] and words[-2]
        if len(words) > 4:
            item = " ".join(words[3:-1])
        else:
            item = "misc"

        return {
            "action": "add_udhaar",
            "customer_name": customer.capitalize(),
            "item": item,
            "amount": amount
        }

    # repayment Ramesh 100
    if words[0] == "repayment":
        if len(words) < 3:
            return {"action": "unknown"}

        customer = words[1]
        try:
            amount = float(words[2])
        except ValueError:
            return {"action": "unknown"}

        return {
            "action": "repayment",
            "customer_name": customer.capitalize(),
            "amount": amount
        }

    return {"action": "unknown"}
