import requests
from pprint import pprint
from datetime import datetime, timedelta

rasa_url = 'http://localhost:5005'
chatwoot_url = 'http://localhost:3000'
chatwoot_bot_token = '4a36A81zfnmswZzjPVdr7drF'

# Dictionary to store the last processed timestamp for each conversation ID
last_processed_timestamp = {}


def should_skip_processing(conversation_id):
    if conversation_id in last_processed_timestamp:
        last_processed_time = last_processed_timestamp[conversation_id]
        current_time = datetime.now()
        time_difference = current_time - last_processed_time

        # If the conversation was processed within the last 5 seconds, skip processing
        if time_difference < timedelta(seconds=5):
            return True

    return False

def send_to_bot(conversation, message):
    data = {
        "sender": conversation,
        "message": message,
    }
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

    r = requests.post(f'{rasa_url}/webhooks/rest/webhook',
                      json=data, headers=headers)
    return r.json()[0]['text']


def send_to_chatwoot(account, conversation, message):
    queue = []
    data = {
        'content': message
    }
    url = f"{chatwoot_url}/api/v1/accounts/{account}/conversations/{conversation}/messages"
    # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++",type(conversation))
    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "api_access_token": f"{chatwoot_bot_token}"}

    r = requests.post(url,
                      json=data, headers=headers)
    
    return r.json()


from flask import Flask, request
app = Flask(__name__)


@app.route('/rasa', methods=['POST'])
def rasa():
        
    create_message = ''
    data = request.get_json()
    # pprint(data)
    message_type = data['message_type']
    pprint(data)

    message = data['content']
    conversation = data['conversation']['id']
    user_specific = data['conversation']['id']

    print("Conversation Id",conversation)
    contact = data['sender']['id']
    account = data['account']['id']
    print("Account id",account)

    status = data['conversation']['status']
    # if(status == 'pending'):
    #     if(message_type == "incoming"):
    if should_skip_processing(conversation):
        return {"status": "skipped"}
    
    last_processed_timestamp[conversation] = datetime.now()
    # print(data)
    if status == 'pending' and message_type == "incoming":        
        bot_response = send_to_bot(conversation, message)
        create_message = send_to_chatwoot(
            account, conversation, bot_response)
    return create_message

if __name__ == '__main__':
    app.run(debug=1)
    # print(send_to_chatwoot(2,12,'3'))