import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import time

SLACK_BOT_TOKEN = '' # Replace with your bot token
CHANNEL_ID = '' # Replace with your channel ID

success_message = '' # Replace with your message

def get_most_recent_message(channel_id):
    client = WebClient(token=os.environ[SLACK_BOT_TOKEN])
    
    try:
        response = client.conversations_history(channel=channel_id, limit=1)
        message = response['messages'][0]['text']
        return message
    except SlackApiError as e:
        print(f"Error retrieving messages: {e.response['error']}")
        return None

def send_message_to_slack(channel_id, message):
    client = WebClient(token=os.environ[SLACK_BOT_TOKEN])
            
    try:
        response = client.chat_postMessage(channel=channel_id, text=message)
        return response
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")
        return None

def happiness_score(message):
    positive_keywords = ['achieved', 'finished', 'completed', 'accomplished', 'succeeded', 'won', 'done', 'submitted', 'approved', 'accepted', 'passed', 'good job', 'great', 'congratulations', 'congrats', 'well done', 'awesome', 'amazing', 'fantastic', 'excellent', 'wonderful', 'superb', 'outstanding', 'terrific', 'brilliant', 'impressive', 'impressed', 'proud of you', 'you nailed it', 'awesome', 'amazing', 'fantastic', 'outstanding', 'yay', 'we are so back']
    score = 0
    
    for word in positive_keywords:
        if word in message.lower():
            score += 10
    
    return score

while True:
    time.sleep(3)
    message = get_most_recent_message(CHANNEL_ID)
    score = happiness_score(message)
    
    if score > 0:
        send_message_to_slack(CHANNEL_ID, success_message)