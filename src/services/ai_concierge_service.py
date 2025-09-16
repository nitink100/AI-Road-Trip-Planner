import os

# The directory where the AI's knowledge files are stored
KNOWLEDGE_BASE_DIR = 'knowledge_base'

class AiConcierge:
    """
    Handles all AI-powered suggestions using a Retrieval-Augmented Generation (RAG) pattern.
    """
    def __init__(self, gemini_client):
        """
        Initializes the AI Concierge.

        Args:
            gemini_client: An instance of the GeminiClient class.
        """
        self.gemini_client = gemini_client
        self.knowledge_base = self._load_knowledge_base()
        if self.knowledge_base and self.knowledge_base != "No local knowledge base found.":
            print(f"🧠 AI Concierge knowledge base loaded successfully.")

    def _load_knowledge_base(self):
        """
        Loads all .txt files from the knowledge base directory into a single string.
        This represents the "Retrieval" part of RAG.
        """
        kb_content = ""
        if not os.path.exists(KNOWLEDGE_BASE_DIR):
            print(f"Warning: Knowledge base directory '{KNOWLEDGE_BASE_DIR}' not found.")
            return "No local knowledge base available."

        for filename in os.listdir(KNOWLEDGE_BASE_DIR):
            if filename.endswith(".txt"):
                try:
                    with open(os.path.join(KNOWLEDGE_BASE_DIR, filename), 'r', encoding='utf-8') as f:
                        kb_content += f.read() + "\n\n"
                except Exception as e:
                    print(f"Warning: Could not read file {filename}. Error: {e}")
        
        return kb_content if kb_content else "No local knowledge base found."

    def provide_suggestions(self, itinerary, interests=None, budget=None):
        """
        Constructs a prompt with context, generates travel suggestions, and returns them.
        """
        print("\n🤖 What would you like to know about your trip?")
        query = input("Example: 'Suggest a good place for lunch near the destination.'\n> ")

        # --- Augment the prompt with all available context ---
        prompt = f"""
        You are a friendly and expert travel assistant. Your goal is to provide a helpful and concise recommendation based on the user's trip plan and their query.

        **Trip Details:**
        - Origin: {itinerary['summary']['origin']}
        - Destination: {itinerary['summary']['destination']}

        **User Preferences:**
        - Interests: {interests or 'Not specified'}
        - Daily Food Budget: ${budget or 'Not specified'}

        **Provided Context from my Knowledge Base:**
        ---
        {self.knowledge_base}
        ---

        **User's Question:**
        "{query}"

        **Your Recommendation:**
        """
        
        print("\n🤖 Thinking...")
        # --- Generate the response and return it ---
        response = self.gemini_client.generate_content(prompt)
        return response