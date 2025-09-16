# AI-Powered Python Road Trip Planner 🗺️

Built with Python, this smart command-line tool leverages the Google Maps Directions API for routing and the Google Gemini LLM for AI-powered enrichment. The application functions as a travel concierge by implementing a Retrieval-Augmented Generation (RAG) pipeline to deliver intelligent, context-aware suggestions beyond simple navigation.

---

## ✨ Features

- **Dynamic Itinerary Generation:** Plan trips with custom starting points, destinations, and departure times.
- **Google Maps Integration:** Fetches real-time route data, including distance, duration, and step-by-step instructions.
- **AI Travel Concierge:** Ask for recommendations about your trip! The AI can suggest interesting stops, restaurants, or activities based on your interests and budget.
- **Retrieval-Augmented Generation (RAG):** The AI's suggestions are grounded in a local knowledge base, powered by a vector database for intelligent, semantic searching. This ensures recommendations are relevant and context-aware.
- **Personalized Planning:** Tailor your trip by providing your interests (e.g., "hiking, history") and daily budget to get customized suggestions.
- **Custom Rest Periods:** Define a daily "sleep time" to automatically pause the itinerary, ensuring a realistic travel schedule for multi-day trips.
- **Save & Export:** Save your complete itinerary to a formatted text file for offline access.

---

## 🛠️ Tech Stack

- **Language:** Python
- **LLM:** Google Gemini API
- **API Clients:** `requests` for Google Maps, `google-generativeai` for Gemini
- **Vector Database:** FAISS for local, efficient similarity search
- **API Key Management:** `python-dotenv`
- **Primary Services:** Google Maps Directions API, Google AI Platform

---

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

- Python (version 3.8 or newer recommended)
- Pip (Python package installer)
- A Google Maps API Key and a Gemini API Key

### Installation

1.  **Get your API Keys:**
    - **Google Maps:** Enable the **Directions API** in the [Google Cloud Console](https://console.cloud.google.com/) and create an API key.
    - **Gemini:** Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

2.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/ai-python-trip-planner.git](https://github.com/your-username/ai-python-trip-planner.git)
    cd ai-python-trip-planner
    ```

3.  **Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up your environment variables:**
    - Create a file named `.env` in the root of the project.
    - Add your API keys to it (use `.env.example` as a template):
      ```
      GOOGLE_MAPS_API_KEY="PASTE_YOUR_MAPS_KEY_HERE"
      GEMINI_API_KEY="PASTE_YOUR_GEMINI_KEY_HERE"
      ```

6.  **Build your Knowledge Base:**
    - Add `.md` or `.txt` files with travel information into the `knowledge_base/` directory. The more information you provide, the smarter the AI concierge will be.

---

## 🏃 How to Run

Execute the main script from your terminal. The application will first build the vector database from your knowledge base and then guide you through planning your trip.

```bash
python main.py


