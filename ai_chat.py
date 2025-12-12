# ai_chat.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_ai(user_message: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are SahaYogi, an AI assistant for Indian shopkeepers. Be simple, helpful, and practical."},
            {"role": "user", "content": user_message},
        ]
    )

    return response.choices[0].message.content