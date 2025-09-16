from datetime import datetime

def get_trip_details():
    """
    Gathers all necessary trip planning information from the user,
    including new details like interests and budget.
    """
    print("\n" + "="*50)
    print("      Welcome to the AI Road Trip Planner!      ")
    print("="*50)
    
    # --- Core Trip Details ---
    origin = _prompt("Enter the starting location:")
    destination = _prompt("Enter the ending location:")
    start_time = _get_start_time()
    transport_mode = _get_transport_mode()
    
    # --- Personalization Details for AI ---
    print("\n--- Personalize Your Trip ---")
    interests = _prompt("List some interests (e.g., hiking, history, museums):", is_required=False)
    budget = _prompt("What is your daily budget for food? (e.g., 50, 100):", is_required=False)
    
    # --- Scheduling Details ---
    sleep_period = _get_sleep_period()
    
    return {
        "origin": origin,
        "destination": destination,
        "start_time": start_time,
        "transport_mode": transport_mode,
        "interests": interests,
        "budget": budget,
        "sleep_period": sleep_period
    }

def display_itinerary(itinerary):
    """Formats and prints the final trip itinerary to the console."""
    summary = itinerary['summary']
    print("\n" + "="*50)
    print("      Your Trip Itinerary      ")
    print("="*50)
    print(f"From: {summary['origin']}")
    print(f"To:   {summary['destination']}")
    print(f"Total Distance: {summary['distance']}")
    print(f"Estimated Duration: {summary['duration']}")
    print(f"Departure: {summary['start_time']}")
    print("-" * 50)

    for step in itinerary['steps']:
        print(f"\nStep {step['number']}:")
        print(f"  -> Instruction: {step['instructions']}")
        print(f"  -> Distance: {step['distance']}")
        print(f"  -> Travel Time: {step['start_time']} to {step['end_time']}")
    
    print("\n" + "="*50)

def display_ai_response(response):
    """Formats and prints the AI's suggestions."""
    print("\n--- 🤖 AI Travel Concierge ---")
    print(response)
    print("-----------------------------\n")

def display_error(response):
    """Displays a user-friendly error message if an API call fails."""
    status = response.get('status', 'UNKNOWN_ERROR') if response else 'NO_RESPONSE'
    print(f"\n--- Error ---")
    print(f"Could not retrieve route. Status: {status}")
    if response and response.get('available_travel_modes'):
        modes = ", ".join(response['available_travel_modes'])
        print(f"Available modes for this route might be: {modes}")

def ask_for_ai_suggestions():
    """Asks the user if they want AI-powered suggestions."""
    return _prompt_yes_no("\nWould you like some AI-powered suggestions for your trip?")

def ask_to_save_itinerary():
    """Asks the user if they want to save the itinerary to a file."""
    return _prompt_yes_no("Would you like to save this itinerary to a file?")

def continue_prompt():
    """Asks the user if they want to plan another trip."""
    return _prompt_yes_no("\nPlan another trip?")

def say_goodbye():
    """Prints a farewell message."""
    print("\nHappy travels!")

# --- Private Helper Functions ---

def _prompt(message, is_required=True):
    """A robust helper to get input from the user."""
    while True:
        response = input(f"{message} ").strip()
        if response:
            return response
        if is_required:
            print("This field cannot be empty. Please try again.")
        else:
            return None # Return None if the field is optional and empty

def _prompt_yes_no(message):
    """A helper to get a 'yes' or 'no' answer."""
    while True:
        response = input(f"{message} (y/n): ").lower()
        if response in ['y', 'yes']:
            return True
        if response in ['n', 'no']:
            return False
        print("Invalid input. Please enter 'y' or 'n'.")

def _get_start_time():
    """Gets a valid start time from the user."""
    while True:
        choice = input("Is this trip starting now or in the future? (now/future): ").lower()
        if choice == 'now':
            return datetime.now()
        if choice == 'future':
            try:
                date_str = _prompt("Enter start date (YYYY-MM-DD):")
                time_str = _prompt("Enter start time (HH:MM in 24-hour format):")
                return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            except ValueError:
                print("Invalid format. Please use YYYY-MM-DD and HH:MM.")
        else:
            print("Invalid choice. Please enter 'now' or 'future'.")

def _get_transport_mode():
    """Gets a valid transport mode from the user."""
    modes = {'1': 'driving', '2': 'bicycling', '3': 'walking', '4': 'transit'}
    while True:
        print("\nSelect transport mode:")
        print("  1. Driving\n  2. Bicycling\n  3. Walking\n  4. Public Transit")
        choice = input("Enter choice (1-4): ")
        if choice in modes:
            return modes[choice]
        print("Invalid choice. Please enter a number from 1 to 4.")

def _get_sleep_period():
    """Gets an optional daily sleep period from the user."""
    if _prompt_yes_no("\nDo you want to set a daily sleep/rest period?"):
        while True:
            try:
                start_str = _prompt("Enter sleep start time (e.g., 22:00):")
                end_str = _prompt("Enter sleep end time (e.g., 06:00):")
                # Parse time strings into time objects
                sleep_start = datetime.strptime(start_str, "%H:%M").time()
                sleep_end = datetime.strptime(end_str, "%H:%M").time()
                return (sleep_start, sleep_end)
            except ValueError:
                print("Invalid time format. Please use HH:MM.")
    return None