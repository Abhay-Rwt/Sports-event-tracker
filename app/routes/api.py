from flask import Blueprint, request, jsonify, current_app
from app.utils.sports_api import get_sports_data, get_api_football_data
import requests
from datetime import datetime, timedelta
import random

api_bp = Blueprint('api', __name__)

@api_bp.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Process the message using the chatbot
    from app.utils.chatbot import get_chatbot_response
    response = get_chatbot_response(message)
    
    return jsonify({'response': response})

@api_bp.route('/sports/events', methods=['GET'])
def get_sports_events():
    sport_type = request.args.get('type', 'all')
    current_app.logger.info(f"Getting sports events for type: {sport_type}")
    
    events = get_sports_data(sport_type)
    
    return jsonify(events)

@api_bp.route('/football/test', methods=['GET'])
def test_football_api():
    """Test route for football API"""
    
    # Directly call the football API function
    events = get_api_football_data('football')
    
    # Return the events data
    return jsonify({
        'count': len(events),
        'events': events
    })

@api_bp.route('/football/alternate', methods=['GET'])
def alternate_football_api():
    """
    Alternate football API using a free public API
    """
    try:
        # Create sample football data directly
        teams = [
            {"name": "Arsenal", "city": "London"},
            {"name": "Manchester United", "city": "Manchester"},
            {"name": "Liverpool", "city": "Liverpool"},
            {"name": "Chelsea", "city": "London"},
            {"name": "Manchester City", "city": "Manchester"},
            {"name": "Tottenham Hotspur", "city": "London"},
            {"name": "Leicester City", "city": "Leicester"},
            {"name": "Everton", "city": "Liverpool"},
            {"name": "West Ham United", "city": "London"},
            {"name": "Aston Villa", "city": "Birmingham"},
            {"name": "Newcastle United", "city": "Newcastle"},
            {"name": "Leeds United", "city": "Leeds"},
            {"name": "Brighton", "city": "Brighton"},
            {"name": "Southampton", "city": "Southampton"},
            {"name": "Brentford", "city": "London"},
            {"name": "Crystal Palace", "city": "London"},
            {"name": "Burnley", "city": "Burnley"},
            {"name": "Watford", "city": "Watford"},
            {"name": "Norwich City", "city": "Norwich"},
            {"name": "Wolverhampton", "city": "Wolverhampton"}
        ]
        
        # Shuffle teams and create matchups
        random.shuffle(teams)
        
        today = datetime.now()
        # Force year to 2024 to avoid system date issues
        today = today.replace(year=2024)
        events = []
        
        # Create 10 sample fixtures
        for i in range(10):
            home_idx = i * 2
            away_idx = i * 2 + 1
            
            if away_idx < len(teams):
                home_team = teams[home_idx]
                away_team = teams[away_idx]
                
                game_date = today + timedelta(days=i)
                
                event = {
                    'id': f"football-alt-{i}",
                    'home_team': home_team.get('name', 'Unknown'),
                    'away_team': away_team.get('name', 'Unknown'),
                    'date': game_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'location': f"{home_team.get('city', '')} Stadium",
                    'status': 'Scheduled',
                    'sport': 'football'
                }
                
                events.append(event)
        
        return jsonify({
            'count': len(events),
            'events': events
        })
            
    except Exception as e:
        current_app.logger.error(f"Error in alternate football API: {str(e)}")
        return jsonify({
            'count': 0,
            'events': [],
            'error': str(e)
        }) 