import os
import sys
from dotenv import load_dotenv

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from clients import google_maps_client, gemini_client
from services import trip_planner_service, ai_concierge_service
from ui import command_line_ui

def main():
    """
    Main function to orchestrate the AI Road Trip Planner application.
    """
    load_dotenv()
    maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not maps_api_key or not gemini_api_key:
        print("Error: API keys for Google Maps and Gemini must be set in the .env file.")
        return

    # --- Initialization ---
    try:
        gemini = gemini_client.GeminiClient(gemini_api_key)
        concierge = ai_concierge_service.AiConcierge(gemini)
        print("AI Concierge is ready.")
    except Exception as e:
        print(f"Failed to initialize AI systems: {e}")
        return

    # --- Main Application Loop ---
    while True:
        user_input = command_line_ui.get_trip_details()

        print("\nFetching route from Google Maps...")
        maps_response = google_maps_client.fetch_directions(
            maps_api_key,
            origin=user_input["origin"],
            destination=user_input["destination"],
            mode=user_input["transport_mode"]
        )

        if maps_response and maps_response.get("status") == "OK":
            itinerary = trip_planner_service.generate_itinerary(
                maps_response,
                user_input["start_time"],
                user_input.get("sleep_period")
            )
            command_line_ui.display_itinerary(itinerary)

            if command_line_ui.ask_for_ai_suggestions():
                # The service now RETURNS the suggestion instead of printing it
                suggestion = concierge.provide_suggestions(itinerary)
                # Main tells the UI to display the result
                command_line_ui.display_ai_response(suggestion)
            
            if command_line_ui.ask_to_save_itinerary():
                trip_planner_service.save_itinerary_to_file(itinerary)
        else:
            command_line_ui.display_error(maps_response)

        if not command_line_ui.continue_prompt():
            break
    
    command_line_ui.say_goodbye()

if __name__ == "__main__":
    main()