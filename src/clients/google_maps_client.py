import requests

DIRECTIONS_API_URL = "https://maps.googleapis.com/maps/api/directions/json"

def fetch_directions(api_key, origin, destination, mode):
    """Fetches route information from the Google Maps Directions API."""
    params = {
        "origin": origin,
        "destination": destination,
        "mode": mode,
        "key": api_key
    }
    try:
        response = requests.get(DIRECTIONS_API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Google Maps API: {e}")
        return None
