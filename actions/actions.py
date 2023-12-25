
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from pprint import pprint

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_human_handoff"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Please wait still we connect to agent.")

        conversation_id = int(tracker.sender_id)

        ##URL##
        url = f"http://localhost:3000/api/v1/accounts/1/conversations/{conversation_id}/toggle_status"

        ##DATA##
        data = {
            "status": "open"
        }
        ##HEADERS##
        headers = {
            "api_access_token": "4a36A81zfnmswZzjPVdr7drF",
            "Content-Type": "application/json"  # Adjust the content type as needed
        }
        ##REQUEST##
        response = requests.post(url, json=data, headers=headers,verify=False)

        # Check the response
        if response.status_code == 200:
            print("POST request was successful!")
            print("Response JSON:", response.json())
        else:
            print("POST request failed with status code:", response.status_code)
            print("Response content:", response.text)

        return []
