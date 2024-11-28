# fulfillment.py

from flask import Flask, request, jsonify
import requests
from config import SPORTS_API_KEY

app = Flask(__name__)

# Function to fetch upcoming sports events
def get_upcoming_events(sport="basketball"):
    url = f"https://api.sportsdata.io/v3/{sport}/scores/json/GamesByDate/{sport}/2024-11-28"
    headers = {"Ocp-Apim-Subscription-Key": SPORTS_API_KEY}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        events = response.json()
        return events
    return []

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    
    # Get the intent name from the Dialogflow request
    intent = req['queryResult']['intent']['displayName']
    
    if intent == 'UpcomingGamesIntent':
        events = get_upcoming_events("basketball")  # Example: Fetch basketball games
        if events:
            message = "Upcoming Basketball Games:\n"
            for event in events[:5]:  # Limit to the first 5 events
                message += f"{event['HomeTeam']} vs {event['AwayTeam']} on {event['DateTime']}\n"
            return jsonify({
                "fulfillmentText": message
            })
        else:
            return jsonify({
                "fulfillmentText": "Sorry, I couldn't fetch the events at the moment."
            })
    
    return jsonify({"fulfillmentText": "I'm not sure what you're asking."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
