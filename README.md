# Travel Concierge App (Cora)

## Overview

**Cora** is an AI-powered travel concierge that crafts hyper-personalised, day-by-day itineraries based on user preferences in films, music, and cuisine. It integrates multiple APIs, Qloo Taste AI™, Groq LLM, and Pexels, to deliver culturally rich, visually engaging plans tailored to each user’s inferred emotional tone.

## Features

- Dynamic, tone-infused itinerary generation (adventurous, romantic, minimalist, energetic)  
- Cultural recommendation enrichment via Qloo Taste AI™  
- Poetic itinerary creation using Groq's LLM (`deepseek-r1-distill-llama-70b`)  
- Neighborhood imagery courtesy of Pexels API  
- Mood-setting YouTube playlist links for suggested artists  
- Estimated daily budget in local currency  
- Downloadable, printable PDF via FPDF  
- Graceful handling of sparse inputs and API failures

## Requirements

- Python 3.8+  
- Dependencies listed in `requirements.txt`:
  ```
  streamlit
  requests
  fpdf
  toml
  ```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ojumah20/Cora--Travel-Concierge.git
   cd travel-concierge
   ```
2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Configure API keys** in `~/.streamlit/secrets.toml` (see below).

## Configuration (`secrets.toml`)

Create a file at `.streamlit/secrets.toml` containing:
```toml
QLOO_API_KEY = "<your_qloo_key>"
GROQ_API_KEY = "<your_groq_key>"
GROQ_MODEL   = "deepseek-r1-distill-llama-70b"
PEXELS_API_KEY = "<your_pexels_key>"
```

## Project Structure

```
├── app.py                   # Main Streamlit interface (formerly main page)
├── config.py                # Holds API keys and model configurations
├── qloo.py                  # Qloo API integration functions
├── main.py                  # Groq LLM itinerary generator
├── images.py                # Pexels API image fetcher
├── pdf_downloading.py       # FPDF export logic
├── .streamlit/              # Streamlit configuration and secrets
│   └── secrets.toml         # Secure storage for API keys
├── requirements.txt         # Python dependencies
└── README.md                # This documentation
```

## Usage

```bash
streamlit run app.py
```

1. Open the local URL in your browser.  
2. Enter destination, trip length, and your favorite films, artists, and cuisines.  
3. Click **Generate Itinerary**.  
4. View the personalized plan with neighborhood images and playlist links.  
5. Download as PDF for offline use.

## Deployment

We recommend deploying on **Streamlit Cloud**:

1. Push your code to GitHub.  
2. Add API keys in the Streamlit Cloud app settings (Secrets).  
3. Connect your repo in the Streamlit Cloud dashboard.  
4. Enable auto-deploy on push to the `main` branch.

## Contributing

Contributions are welcome! Please open issues or pull requests for enhancements, bug fixes, or new features.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
