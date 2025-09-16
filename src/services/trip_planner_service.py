import re
import json
from datetime import datetime, timedelta

def generate_itinerary(maps_response, start_time, sleep_period=None):
    """
    Converts Google Maps API response into a structured itinerary.
    
    Args:
        maps_response: Response from Google Maps Directions API
        start_time: datetime object for trip start
        sleep_period: Optional tuple of (sleep_start, sleep_end) times
    
    Returns:
        dict: Structured itinerary with summary and step-by-step details
    """
    if not maps_response or maps_response.get("status") != "OK":
        return None
    
    route = maps_response["routes"][0]
    leg = route["legs"][0]
    
    # Extract summary information
    summary = {
        "origin": leg["start_address"],
        "destination": leg["end_address"],
        "distance": leg["distance"]["text"],
        "duration": leg["duration"]["text"],
        "start_time": start_time.strftime("%Y-%m-%d %H:%M")
    }
    
    # Process each step
    steps = []
    current_time = start_time
    
    for i, step in enumerate(leg["steps"]):
        # Clean HTML instructions using regex
        instructions = step['html_instructions']
        instructions = instructions.replace('<div style="font-size:0.9em">', ' (').replace('</div>', ')')
        instructions = re.sub(r'<.*?>', '', instructions)  # Remove all HTML tags
        instructions = re.sub(r'\s+', ' ', instructions).strip()  # Clean up whitespace
        
        # Calculate step duration
        step_duration_seconds = step["duration"]["value"]
        step_duration = timedelta(seconds=step_duration_seconds)
        
        # Handle sleep periods if specified
        if sleep_period:
            current_time = _handle_sleep_period(current_time, sleep_period)
        
        end_time = current_time + step_duration
        
        step_info = {
            "number": i + 1,
            "instructions": instructions,
            "distance": step["distance"]["text"],
            "duration": step["duration"]["text"],
            "start_time": current_time.strftime("%H:%M"),
            "end_time": end_time.strftime("%H:%M"),
            "travel_mode": step.get("travel_mode", "UNKNOWN")
        }
        
        steps.append(step_info)
        current_time = end_time
    
    return {
        "summary": summary,
        "steps": steps,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def _handle_sleep_period(current_time, sleep_period):
    """
    Adjusts current time if it falls within the sleep period.
    
    Args:
        current_time: Current datetime
        sleep_period: Tuple of (sleep_start_time, sleep_end_time)
    
    Returns:
        datetime: Adjusted time if necessary
    """
    sleep_start, sleep_end = sleep_period
    current_time_only = current_time.time()
    
    # Check if current time falls within sleep period
    if sleep_start <= sleep_end:  # Normal case (e.g., 22:00 to 06:00 next day)
        if sleep_start <= current_time_only <= sleep_end:
            # Advance to end of sleep period
            next_day = current_time.date()
            if current_time_only >= sleep_start:
                next_day += timedelta(days=1)
            return datetime.combine(next_day, sleep_end)
    else:  # Sleep period crosses midnight (e.g., 23:00 to 07:00)
        if current_time_only >= sleep_start or current_time_only <= sleep_end:
            # Advance to end of sleep period
            next_day = current_time.date()
            if current_time_only >= sleep_start:
                next_day += timedelta(days=1)
            return datetime.combine(next_day, sleep_end)
    
    return current_time

def save_itinerary_to_file(itinerary, filename=None):
    """
    Saves the itinerary to a JSON file.
    
    Args:
        itinerary: The itinerary dictionary
        filename: Optional custom filename
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"itinerary_{timestamp}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(itinerary, file, indent=2, ensure_ascii=False)
        print(f"✓ Itinerary saved to: {filename}")
        return True
    except Exception as e:
        print(f"✗ Error saving itinerary: {e}")
        return False

def load_itinerary_from_file(filename):
    """
    Loads an itinerary from a JSON file.
    
    Args:
        filename: Path to the JSON file
    
    Returns:
        dict: The itinerary dictionary or None if error
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"✗ Error loading itinerary: {e}")
        return None