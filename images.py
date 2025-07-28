import requests
import streamlit as st

PEXELS_API_KEY = st.secrets["PEXELS_API_KEY"]
# --- Image from Pexels ---
def get_neighborhood_image(query):
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        photos = data.get("photos", [])
        if photos:
            return photos[0]["src"]["landscape"]
    return None