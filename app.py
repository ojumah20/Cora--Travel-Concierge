import streamlit as st
import re
from qloo import fetch_qloo_recommendations
from images import get_neighborhood_image
from pdf_downloading import export_itinerary_to_pdf
from main import generate_itinerary


# session state initialization
defaults = {
    "scroll_to_itinerary": False,
    "generated_itinerary": "",
    "pdf_buffer": None,
    "qloo_results": {}
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --- Cleaning Output ---
def clean_llm_output(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

# --- Extract Neighborhoods ---
def extract_neighborhoods(itinerary_text):
    return re.findall(r"Day\s+\d+:\s+(.+?)(?=\n|$)", itinerary_text)




# --- Streamlit App ---
st.set_page_config(page_title="Travel Concierge", page_icon="🎒")

st.markdown(
    """
    <h1 style='text-align: center;'>🎒 Hyper-Personalized Travel Concierge</h1>
    <p style='text-align: center; font-size: 18px;'>Transform your cultural preferences into bespoke travel experiences</p>
    <br> </br>
    """,
    unsafe_allow_html=True
)

with st.form("itinerary_form"):
    st.markdown("Tell us your cultural tastes. We'll craft the perfect itinerary just for you.")
    destination = st.text_input("Destination City", placeholder="e.g. Paris")
    trip_days = st.slider("How many days is your trip?", min_value=1, max_value=7, value=3)
    films = st.text_area("Your Favorite Films", placeholder="e.g. Amélie, The Grand Budapest Hotel")
    artists = st.text_area("Your Favorite Music Artists", placeholder="e.g. Norah Jones, Chet Baker")
    cuisines = st.text_area("Favorite Cuisines", placeholder="e.g. French, Vietnamese")
    submitted = st.form_submit_button("Generate Itinerary")

if submitted:
    with st.spinner("Fetching recommendations..."):
        user_data = {
            "films": [f.strip() for f in films.split(",") if f.strip()],
            "artists": [a.strip() for a in artists.split(",") if a.strip()],
            "cuisines": [c.strip() for c in cuisines.split(",") if c.strip()],
            "destination": destination.strip(),
            "user_days": trip_days
        }

        qloo_results = {
            "films": fetch_qloo_recommendations("movies", user_data["films"]),
            "artists": fetch_qloo_recommendations("music", user_data["artists"]),
            "cuisines": fetch_qloo_recommendations("dining", user_data["cuisines"])
        }

        raw_itinerary = generate_itinerary(user_data, qloo_results)
        itinerary = clean_llm_output(raw_itinerary)
        pdf_buffer = export_itinerary_to_pdf(itinerary)

        st.session_state.generated_itinerary = itinerary
        st.session_state.pdf_buffer = pdf_buffer
        st.session_state.qloo_results = qloo_results
        st.session_state.scroll_to_itinerary = True

        st.rerun()

if st.session_state.scroll_to_itinerary:
    st.toast("✨ Your personalized itinerary is ready!")

    with st.expander("📜 Tap to View Itinerary", expanded=True):
        st.markdown(st.session_state.generated_itinerary)

        neighborhoods = extract_neighborhoods(st.session_state.generated_itinerary)
        for neighborhood in neighborhoods:
            img_url = get_neighborhood_image(f"{neighborhood} {destination}")
            if img_url:
                st.image(img_url, caption=f"{neighborhood}", use_container_width=True)

        if st.session_state.qloo_results.get("artists"):
            st.markdown("🎵 **Suggested Artists & YouTube Links:**")
            for artist in st.session_state.qloo_results["artists"]:
                name = artist.get("name", "")
                if name:
                    link = f"https://www.youtube.com/results?search_query={'+'.join(name.split())}+playlist"
                    st.markdown(f"- [{name}]({link})")

    st.download_button(
        "📄 Download as PDF",
        data=st.session_state.pdf_buffer.getvalue(),
        file_name="itinerary.pdf",
        mime="application/pdf"
    )

    st.session_state.scroll_to_itinerary = False
