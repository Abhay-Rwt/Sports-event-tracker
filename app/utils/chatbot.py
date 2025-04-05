import os
import json
import re
from dotenv import load_dotenv
from datetime import datetime
import requests
from .sports_api import get_sports_data

# Load environment variables
load_dotenv(override=True)  # Force reload environment variables

# Debugging: Print all environment variables for OpenRouter
print("Reloading environment variables...")
print(f"OPENROUTER_API_KEY from env: {os.environ.get('OPENROUTER_API_KEY', '')[:10]}...")

# Set up API keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
OPENROUTER_API_BASE = os.getenv('OPENROUTER_API_BASE', 'https://openrouter.ai/api/v1')
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'deepseek/deepseek-r1:free')

print(f"OpenAI API Key (first 5 chars): {OPENAI_API_KEY[:5] if OPENAI_API_KEY else 'Not set'}")
print(f"OpenRouter API Key (first 5 chars): {OPENROUTER_API_KEY[:5] if OPENROUTER_API_KEY else 'Not set'}")
print(f"OpenRouter API Base: {OPENROUTER_API_BASE}")
print(f"OpenRouter Model: {OPENROUTER_MODEL}")

# Initialize API client variables
openai_client = None
use_openrouter = False

# Flag to track if we properly initialized any API
api_initialized = False

# Try to set up the OpenAI client if API key is available
if OPENAI_API_KEY:
    try:
        # Import OpenAI and initialize client
        import openai
        from openai import OpenAI
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        # Test the API with a small request
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print("OpenAI API connection successful")
        api_initialized = True
    except Exception as e:
        print(f"Error initializing OpenAI client: {str(e)}")
        OPENAI_API_KEY = None
        openai_client = None

# Check if OpenRouter API key is available
if OPENROUTER_API_KEY:
    try:
        # Print full API key for debugging (only first 10 chars for security)
        print(f"Using OpenRouter API Key: {OPENROUTER_API_KEY[:10]}...")
        print(f"OpenRouter API Key length: {len(OPENROUTER_API_KEY)}")
        
        # Test the OpenRouter API using the exact format provided by the user
        print(f"OpenRouter API Key is set. Testing connection with DeepSeek R1...")
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://www.plantai.com",
            "X-Title": "Plant AI",
            "Content-Type": "application/json"
        }
        
        # Use the same model as specified in the environment
        data = {
            "model": OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": "Hello"}]
        }
        
        print(f"Sending test request to OpenRouter with model {OPENROUTER_MODEL}...")
        print(f"Request URL: {OPENROUTER_API_BASE}/chat/completions")
        print(f"Auth header: Bearer {OPENROUTER_API_KEY[:10]}...")
        
        response = requests.post(
            f"{OPENROUTER_API_BASE}/chat/completions",
            headers=headers,
            json=data
        )
        
        print(f"OpenRouter response status: {response.status_code}")
        
        if response.status_code == 200:
            response_text = response.text[:200] + "..." if len(response.text) > 200 else response.text
            print(f"OpenRouter response content: {response_text}")
            print("OpenRouter API connection successful")
            use_openrouter = True
            api_initialized = True
        else:
            print(f"OpenRouter API error: {response.text}")
    except Exception as e:
        print(f"Error connecting to OpenRouter API: {str(e)}")
        print(f"Exception type: {type(e)}")
        if hasattr(e, '__traceback__'):
            import traceback
            print(f"Traceback: {traceback.format_tb(e.__traceback__)}")

if not api_initialized:
    print("WARNING: No AI API services were successfully initialized. Using rule-based processing only.")

# Intent patterns for sports queries
INTENT_PATTERNS = {
    'get_events': [
        r'(?i)what\s+(?:sports\s+)?events\s+(?:are\s+)?(?:there|happening|scheduled)(?:\s+today|\s+this\s+week|\s+this\s+month)?',
        r'(?i)show\s+me\s+(?:all\s+)?(?:the\s+)?(?:sports\s+)?events(?:\s+today|\s+this\s+week|\s+this\s+month)?',
        r'(?i)list\s+(?:all\s+)?(?:the\s+)?(?:sports\s+)?events(?:\s+today|\s+this\s+week|\s+this\s+month)?'
    ],
    'get_sport_specific_events': [
        r'(?i)what\s+(?:are\s+the\s+)?(\w+)\s+(?:games|events|matches)(?:\s+today|\s+this\s+week|\s+this\s+month)?',
        r'(?i)show\s+me\s+(?:all\s+)?(?:the\s+)?(\w+)\s+(?:games|events|matches)(?:\s+today|\s+this\s+week|\s+this\s+month)?',
        r'(?i)when\s+(?:is|are)\s+the\s+next\s+(\w+)\s+(?:game|event|match)',
        r'(?i)list\s+(?:all\s+)?(?:the\s+)?(\w+)\s+(?:games|events|matches)(?:\s+today|\s+this\s+week|\s+this\s+month)?'
    ],
    'get_team_schedule': [
        r'(?i)when\s+(?:do|does|is|are)\s+(?:the\s+)?([A-Za-z\s]+)(?:\s+play|\s+playing|\s+game|\s+match)',
        r'(?i)what\s+(?:is|are)\s+(?:the\s+)?([A-Za-z\s]+)(?:\s+schedule|\s+games|\s+matches)',
        r'(?i)show\s+me\s+(?:the\s+)?([A-Za-z\s]+)(?:\s+schedule|\s+games|\s+matches)'
    ],
    'general_question': [
        r'(?i).*'  # Catch-all for general questions
    ]
}

# Add new constants after INTENT_PATTERNS
TOPIC_PATTERNS = {
    'sports': [
        r'(?i)sports?',
        r'(?i)match(es)?',
        r'(?i)game(s)?',
        r'(?i)event(s)?',
        r'(?i)tournament(s)?',
        r'(?i)championship(s)?',
        r'(?i)football|soccer|basketball|cricket|baseball|tennis',
        r'(?i)team(s)?',
        r'(?i)play(ing|er)?',
        r'(?i)score(s)?',
        r'(?i)schedule(s)?'
    ],
    'non_sports': [
        r'(?i)joke(s)?',
        r'(?i)funny',
        r'(?i)weather',
        r'(?i)news',
        r'(?i)movie(s)?',
        r'(?i)music',
        r'(?i)restaurant(s)?',
        r'(?i)tell me about',
        r'(?i)how (are|is) you',
        r'(?i)hello|hi|hey',
        r'(?i)thanks?|thank you'
    ]
}

def detect_topic(query):
    """
    Detect if a query is sports-related or not
    
    Args:
        query (str): The user's query
        
    Returns:
        str: 'sports' or 'non_sports'
    """
    for topic, patterns in TOPIC_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, query):
                return topic
    
    # Default to sports if unclear
    return 'sports'

def process_query(query):
    """
    Process a user query and return an appropriate response
    
    Args:
        query (str): The user's query
        
    Returns:
        str: The chatbot's response
    """
    # Check if API keys are available and initialized
    if api_initialized:
        if (OPENAI_API_KEY and openai_client) or (OPENROUTER_API_KEY and use_openrouter):
            try:
                # Use AI models for natural language processing
                print("Using AI processing (OpenAI or OpenRouter)...")
                return process_with_ai(query)
            except Exception as e:
                print(f"Error with AI processing: {str(e)}")
                print(f"Exception type: {type(e)}")
                if hasattr(e, '__traceback__'):
                    import traceback
                    print(f"Traceback: {traceback.format_tb(e.__traceback__)}")
                # Fall back to rule-based processing if AI fails
                return process_with_rules(query)
        else:
            print("No active API clients available despite initialization, using rule-based processing")
            return process_with_rules(query)
    else:
        print("No API initialized, using rule-based processing")
        # Use rule-based processing if no API keys
        return process_with_rules(query)

def process_with_ai(query):
    """
    Process the query using AI models (OpenAI or OpenRouter)
    
    Args:
        query (str): The user's query
        
    Returns:
        str: The chatbot's response
    """
    # Check if query is sports-related
    topic = detect_topic(query)
    
    # Check for specific sports mentions in the query
    is_football_query = re.search(r'(?i)football|soccer|premier\s+league|epl', query) is not None
    is_cricket_query = re.search(r'(?i)cricket|ipl|t20', query) is not None
    is_basketball_query = re.search(r'(?i)basketball|nba', query) is not None
    
    if topic == 'non_sports':
        system_message = (
            "You are a helpful assistant that specializes in sports information. "
            "If asked about non-sports topics, politely redirect the conversation "
            "to sports-related questions. Be friendly but firm about staying on topic."
        )
    else:
        # Get relevant sports data to provide context
        all_events = get_sports_data('all')
        
        # Filter events by sport if the query is specific
        filtered_events = all_events
        
        if is_football_query:
            football_events = get_sports_data('football')
            system_message = (
                f"You are a helpful sports events assistant specializing in football/soccer. "
                f"The user is asking about football/soccer. "
                f"You have access to the following Premier League football events: {json.dumps(football_events[:5])}"
            )
        elif is_cricket_query:
            # Filter for cricket events
            cricket_events = [event for event in all_events if event.get('sport') == 'cricket']
            system_message = (
                f"You are a helpful sports events assistant specializing in cricket. "
                f"The user is asking about cricket. "
                f"You have access to the following cricket events: {json.dumps(cricket_events[:5])}"
            )
        elif is_basketball_query:
            # Filter for basketball events
            basketball_events = [event for event in all_events if event.get('sport') == 'basketball']
            system_message = (
                f"You are a helpful sports events assistant specializing in basketball. "
                f"The user is asking about basketball. "
                f"You have access to the following basketball events: {json.dumps(basketball_events[:5])}"
            )
        else:
            # General sports query
            football_events = get_sports_data('football')
            basketball_events = [event for event in all_events if event.get('sport') == 'basketball']
            cricket_events = [event for event in all_events if event.get('sport') == 'cricket']
            
            sample_events = []
            # Add a sample of each sport
            if football_events and len(football_events) > 0:
                sample_events.append(football_events[0])
            if basketball_events and len(basketball_events) > 0:
                sample_events.append(basketball_events[0])
            if cricket_events and len(cricket_events) > 0:
                sample_events.append(cricket_events[0])
                
            # Format the sports data for the prompt
            system_message = (
                f"You are a helpful sports events assistant. "
                f"You have access to the following sports events from various sports: {json.dumps(sample_events)}"
                f"The full set of events includes football matches from the Premier League, "
                f"basketball games, and cricket matches. Respond to the user's query based on the events data."
            )
    
    try:
        if OPENAI_API_KEY and openai_client:
            # Use OpenAI
            print("Sending request to OpenAI API...")
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": query}
                ],
                max_tokens=150,
                temperature=0.7,
            )
            print("Received response from OpenAI API")
            return response.choices[0].message.content.strip()
        elif OPENROUTER_API_KEY and use_openrouter:
            # Use OpenRouter with DeepSeek R1 following the exact structure from user example
            print("Sending request to OpenRouter API with DeepSeek R1...")
            print(f"Using current OpenRouter API key: {OPENROUTER_API_KEY[:10]}...")
            print(f"OpenRouter API key length: {len(OPENROUTER_API_KEY)}")
            
            # Create headers using exact same format as user example
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://www.plantai.com",
                "X-Title": "Plant AI",
                "Content-Type": "application/json"
            }
            
            # Add system message to the array
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": query}
            ]
            
            # Create the request body exactly as in the user example
            data = {
                "model": OPENROUTER_MODEL,
                "messages": messages
            }
            
            print(f"OpenRouter request URL: {OPENROUTER_API_BASE}/chat/completions")
            print(f"Auth header: Bearer {OPENROUTER_API_KEY[:10]}...")
            
            # Make the API request
            response = requests.post(
                f"{OPENROUTER_API_BASE}/chat/completions",
                headers=headers,
                json=data
            )
            
            print(f"OpenRouter response status: {response.status_code}")
            
            if response.status_code == 200:
                print("Received successful response from OpenRouter API")
                response_json = response.json()
                
                # Extract the response content
                if 'choices' in response_json and len(response_json['choices']) > 0:
                    if 'message' in response_json['choices'][0] and 'content' in response_json['choices'][0]['message']:
                        return response_json['choices'][0]['message']['content'].strip()
                
                # If we couldn't parse the response properly
                print("Couldn't extract content from response, falling back to rule-based")
                return process_with_rules(query)
            else:
                print(f"OpenRouter API error: {response.text}")
                return process_with_rules(query)
        else:
            print("No API clients available")
            return process_with_rules(query)
    except Exception as e:
        print(f"AI API error: {e}")
        print(f"Exception type: {type(e)}")
        if hasattr(e, '__traceback__'):
            import traceback
            print(f"Traceback: {traceback.format_tb(e.__traceback__)}")
        # Fall back to rule-based processing if AI fails
        return process_with_rules(query)

# Rename the old function name to match our new naming
def process_with_openai(query):
    """
    Legacy function - redirects to process_with_ai
    """
    return process_with_ai(query)

def process_with_rules(query):
    """
    Process the query using rule-based pattern matching
    
    Args:
        query (str): The user's query
        
    Returns:
        str: The chatbot's response
    """
    # Special handling for EPL / Premier League queries
    if re.search(r'(?i)EPL|Premier League|upcoming match', query):
        events = get_sports_data('football')
        epl_events = [event for event in events if event.get('competition', '').lower() == 'premier league']
        if epl_events:
            return format_events_response(epl_events, 'Premier League')
        else:
            return format_events_response(events, 'football')
    
    # Check if query is sports-related
    topic = detect_topic(query)
    
    if topic == 'non_sports':
        # Handle common non-sports queries
        if re.search(r'(?i)joke', query):
            return "I'm a sports information assistant. Instead of jokes, I can tell you about upcoming sports events! Would you like to know what games are happening soon?"
        elif re.search(r'(?i)how are you|how do you do', query):
            return "I'm functioning well, thank you! I'm here to help with sports information. What sports events would you like to know about today?"
        elif re.search(r'(?i)hello|hi|hey', query):
            return "Hello! I'm your sports events assistant. I can help you find information about upcoming games, teams, and sports events. What would you like to know about?"
        elif re.search(r'(?i)thanks|thank you', query):
            return "You're welcome! I'm happy to help with any sports information you need. Is there a specific team or sport you're interested in?"
        else:
            return "I'm a sports event tracker chatbot focused on providing information about sports. I can tell you about upcoming events, team schedules, or specific sports like football, basketball, or cricket. How can I help you with sports today?"
    
    # Continue with existing sports-related query handling
    # Check for intents
    intent, params = extract_intent(query)
    
    if intent == 'get_events':
        events = get_sports_data('all')
        return format_events_response(events, 'all')
    
    elif intent == 'get_sport_specific_events':
        sport_type = params.get('sport_type', '').lower()
        valid_sports = ['football', 'basketball', 'baseball']
        
        if sport_type in valid_sports:
            events = get_sports_data(sport_type)
            return format_events_response(events, sport_type)
        else:
            return f"I don't have information about {sport_type} events at the moment. I currently track football, basketball, and baseball events."
    
    elif intent == 'get_team_schedule':
        team_name = params.get('team_name', '').lower()
        all_events = get_sports_data('all')
        team_events = []
        
        for event in all_events:
            home_team = event.get('home_team', '').lower()
            away_team = event.get('away_team', '').lower()
            
            if team_name in home_team or team_name in away_team:
                team_events.append(event)
        
        if team_events:
            return format_team_events_response(team_events, team_name)
        else:
            return f"I couldn't find any scheduled events for {team_name}. Please check the team name or try another team."
    
    else:  # general_question
        return "I'm a sports event tracker chatbot. You can ask me about upcoming sports events, schedules for specific teams, or events for specific sports like football, basketball, or baseball. How can I help you today?"

def extract_intent(query):
    """
    Extract the intent and parameters from the user query
    
    Args:
        query (str): The user's query
        
    Returns:
        tuple: (intent_name, parameters)
    """
    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            match = re.search(pattern, query)
            if match:
                if intent == 'get_sport_specific_events' and match.group(1):
                    return intent, {'sport_type': match.group(1)}
                elif intent == 'get_team_schedule' and match.group(1):
                    return intent, {'team_name': match.group(1)}
                return intent, {}
    
    # Default to general question if no pattern matches
    return 'general_question', {}

def format_events_response(events, sport_type):
    """
    Format the events data into a readable response
    
    Args:
        events (list): List of event dictionaries
        sport_type (str): Type of sport
        
    Returns:
        str: Formatted response
    """
    if not events:
        return f"No {sport_type} events found at the moment. Please check back later."
    
    if sport_type == 'all':
        response = "Here are some upcoming sports events:\n\n"
    else:
        response = f"Here are some upcoming {sport_type} events:\n\n"
    
    # Limit to 5 events to keep response concise
    for i, event in enumerate(events[:5], 1):
        home_team = event.get('home_team', 'Unknown')
        away_team = event.get('away_team', 'Unknown')
        date_str = event.get('date', '')
        location = event.get('location', event.get('venue', 'Unknown venue'))
        status = event.get('status', 'Unknown status')
        competition = event.get('competition', '')
        
        # Format the date if it's provided
        formatted_date = "Date not available"
        try:
            if event.get('ist_date'):
                # Use the pre-formatted IST date if available
                formatted_date = event.get('ist_date')
            elif date_str:
                # Parse the ISO format date
                if 'Z' in date_str:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                else:
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                
                # Format nicely with day of week
                formatted_date = date_obj.strftime('%A, %B %d, %Y at %I:%M %p')
        except Exception as e:
            print(f"Error formatting date: {e}")
            formatted_date = date_str
        
        response += f"{i}. {away_team} at {home_team}\n"
        response += f"   {formatted_date}\n"
        
        if competition:
            response += f"   {competition} - {location} - {status}\n\n"
        else:
            response += f"   {location} - {status}\n\n"
    
    if len(events) > 5:
        response += f"There are {len(events) - 5} more events available. Ask me about a specific sport or team for more details."
    
    return response

def format_team_events_response(events, team_name):
    """
    Format team-specific events into a readable response
    
    Args:
        events (list): List of event dictionaries
        team_name (str): The name of the team
        
    Returns:
        str: Formatted response
    """
    if not events:
        return f"No events found for {team_name} at the moment. Please check back later."
    
    response = f"Here are the upcoming events for {team_name}:\n\n"
    
    # Limit to 5 events to keep response concise
    for i, event in enumerate(events[:5], 1):
        home_team = event.get('home_team', 'Unknown')
        away_team = event.get('away_team', 'Unknown')
        date_str = event.get('date', '')
        location = event.get('location', 'Unknown venue')
        status = event.get('status', 'Unknown status')
        
        # Format the date if it's provided
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            formatted_date = date_obj.strftime('%A, %B %d, %Y at %I:%M %p')
        except:
            formatted_date = date_str
        
        if team_name.lower() in home_team.lower():
            opponent = away_team
            is_home = True
        else:
            opponent = home_team
            is_home = False
        
        if is_home:
            response += f"{i}. vs {opponent} (Home)\n"
        else:
            response += f"{i}. at {opponent} (Away)\n"
        
        response += f"   {formatted_date}\n"
        response += f"   {location} - {status}\n\n"
    
    if len(events) > 5:
        response += f"There are {len(events) - 5} more events scheduled for {team_name}."
    
    return response

# Add the missing function that is being imported in api.py
def get_chatbot_response(message):
    """
    Main entry point for chatbot responses
    
    Args:
        message (str): The user's message
        
    Returns:
        str: The chatbot's response
    """
    return process_query(message) 