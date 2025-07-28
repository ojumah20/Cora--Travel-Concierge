#from config import GROQ_API_KEY, GROQ_MODEL
import requests
import json
import streamlit as st

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GROQ_MODEL = st.secrets["GROQ_MODEL"]
# --- Groq Itinerary Generator ---


def generate_itinerary(user_data, qloo_results):
    filled_fields = {
        "films": bool(user_data['films']),
        "artists": bool(user_data['artists']),
        "cuisines": bool(user_data['cuisines']),
    }
    filled_count = sum(filled_fields.values())

    film_line = f"- Favorite Films: {', '.join(user_data['films'])}" if filled_fields["films"] else ""
    artist_line = f"- Favorite Artists: {', '.join(user_data['artists'])}" if filled_fields["artists"] else ""
    cuisine_line = f"- Favorite Cuisines: {', '.join(user_data['cuisines'])}" if filled_fields["cuisines"] else ""

    inference_hint = {
        1: "Infer their personality tone mostly from the one input provided and skip vague generalizations.",
        2: "Use the two preferences to gently infer personality tone and avoid overfitting.",
        3: "You have enough data to confidently infer the tone and style preferences.",
    }.get(filled_count, "Infer cautiously.")

    prompt = f"""
    Based on the user's cultural preferences, infer their personality tone and generate a poetic {user_data['user_days']}-day travel itinerary.

    {film_line}
    {artist_line}
    {cuisine_line}

    Use Qloo insights for cultural depth: {json.dumps(qloo_results, indent=2)}

    {inference_hint}

    You must:
    - First infer the emotional tone (e.g. romantic, adventurous, minimalist, relaxed)
    - You are a poetic travel concierge.
    - DO NOT output internal thoughts, explanations, or <think> formatting.
    - Only reference {user_data['destination']} in all recommendations.
    - Build a {user_data['user_days']}-day itinerary with this emotional tone:
      * 1 unique neighborhood per day
      * 2 artistic or cultural activities
      * 2 local food experiences
      * 1 mood-setting playlist
      * 1 book suggestion
    - Fully name restaurants and places so users can find them easily.
    - End with a poetic line for the user.
    - At the end, suggest a rough estimated budget per day based on the destination and type of experiences (in local currency if possible).
    """

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]