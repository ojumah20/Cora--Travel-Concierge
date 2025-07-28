import requests
#from config import QLOO_API_KEY
import streamlit as st
QLOO_API_KEY = st.secrets["QLOO_API_KEY"]
# --- Qloo Recommendation Function ---
def fetch_qloo_recommendations(entity_type, names):
    url = f"https://hackathon.api.qloo.com/culture/v1/{entity_type}/recommendations"
    headers = {
        "Authorization": f"Bearer {QLOO_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "entities": names,
        "limit": 5
    }
    response = requests.post(url, headers=headers, json=data)
    try:
        return response.json().get("recommendations", []) or []
    except Exception:
        return []
