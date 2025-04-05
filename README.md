# Sports Event Tracker Chatbot

A web-based chatbot application that allows users to track sports events and ask questions about schedules, teams, and upcoming games.

## Features

- Interactive chatbot for querying sports information
- Real-time sports event tracking
- Filter events by sport type (football, basketball, baseball)
- Responsive web design for desktop and mobile devices
- AI-powered natural language processing using OpenAI (optional)

## Technology Stack

- **Backend**: Python with Flask and Flask-SocketIO
- **Frontend**: HTML, CSS, JavaScript
- **AI**: OpenAI integration (optional)
- **API**: Sports data API integration (configurable)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd sports-event-tracker-chatbot
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file:
   ```
   cp .env.example .env
   ```

6. Edit the `.env` file and add your API keys:
   - `SECRET_KEY`: A random string for Flask session security
   - `OPENAI_API_KEY`: Your OpenAI API key (optional)
   - `SPORTS_API_KEY`: Your sports data API key (optional, mock data is used if not provided)

## Running the Application

1. Run the application:
   ```
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Using the Chatbot

You can ask the chatbot questions like:
- "What sports events are happening this week?"
- "Show me basketball games"
- "When do the Lakers play next?"
- "List football events"

## Customization

### Adding More Sports

To add more sports, modify the `get_mock_sports_data` function in `app/utils/sports_api.py` and add new sport data.

### Changing the AI Model

If you want to use a different AI model, modify the `process_with_openai` function in `app/utils/chatbot.py`.

## License

[MIT License](LICENSE)

## Acknowledgments

- OpenAI for the API integration
- Sports data providers for event information 