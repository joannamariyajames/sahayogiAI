# chatbot_service.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    # This will crash at startup so you notice the problem
    raise ValueError(
        "GEMINI_API_KEY not found. Put it in a .env file or environment variable."
    )

# Configure Gemini client
genai.configure(api_key=API_KEY)

# Use a cheap & fast model
model = genai.GenerativeModel("gemini-flash-latest")


def get_chat_response(user_message: str, shop_context: str = "") -> str:
    """
    Call Gemini and return the chatbot reply.

    user_message: what the shopkeeper asks.
    shop_context: optional extra info/summary about the shop or data.
    """

    user_message = user_message.strip()
    if not user_message:
        return "Please type a question first."

    system_prompt = (
        "You are SahaYOGI, an AI assistant for small Indian shopkeepers. "
        "Explain things in very simple language, short answers, and focus on "
        "shop management, udhaar, sales, and understanding their dashboard."
    )

    if shop_context:
        system_prompt += f"\n\nExtra context about this shop:\n{shop_context}"

    # Easiest way with Gemini: combine system + user into one prompt
    prompt = f"{system_prompt}\n\nUser: {user_message}"

    try:
        response = model.generate_content(prompt)
        # response.text is the combined output as markdown/plain text
        return response.text.strip()
    except Exception as e:
        # Don't expose internals; just show a simple error
        return f"Sorry, I couldn't reach the AI right now. ({e})"