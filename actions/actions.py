
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from pprint import pprint

# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_human_handoff"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Please wait still we connect to agent.")

#         conversation_id = int(tracker.sender_id)

#         ##URL##
#         url = f"http://localhost:3000/api/v1/accounts/1/conversations/{conversation_id}/toggle_status"

#         ##DATA##
#         data = {
#             "status": "open"
#         }
#         ##HEADERS##
#         headers = {
#             "api_access_token": "4a36A81zfnmswZzjPVdr7drF",
#             "Content-Type": "application/json"  # Adjust the content type as needed
#         }
#         ##REQUEST##
#         response = requests.post(url, json=data, headers=headers,verify=False)

#         # Check the response
#         if response.status_code == 200:
#             print("POST request was successful!")
#             print("Response JSON:", response.json())
#         else:
#             print("POST request failed with status code:", response.status_code)
#             print("Response content:", response.text)

#         return []

class ActionAskEmail(Action):
    def name(self) -> Text:
        return "action_ask_email"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        if tracker.get_slot("previous_email"):
            dispatcher.utter_message(template=f"utter_ask_use_previous_email",)
        else:
            dispatcher.utter_message(template=f"utter_ask_email")
        return []

class ActionOpenIncident(Action):
    def name(self) -> Text:
        return "action_open_incident"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        if tracker.get_slot("previous_email"):
            dispatcher.utter_message(template=f"utter_ask_use_previous_email",)
        else:
            dispatcher.utter_message(template=f"utter_ask_email")
        return []



from rasa_sdk.forms import FormValidationAction

class OrderForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_track_order_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["orderno"]

    def slot_mappings(self) -> Dict[Text, Any]:
        return {"orderno": self.from_text(intent="track_order")}

    def validate_orderno(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if not value:
        # Slot is empty, request the user to provide an order number
            dispatcher.utter_message("Please provide an order number.")
            return {"orderno": None}
        # Add your validation logic here (e.g., check if the order number is valid)
        if value.isnumeric() and len(value) == 5:
            # Valid order number
            return {"orderno": value}
        else:
            dispatcher.utter_message("Please provide a valid order number.")
            # Reset the slot if validation fails
            return {"orderno": None}
        

class ActionCheckOrder(Action):
    def name(self) -> Text:
        return "action_check_order"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        orderno = tracker.get_slot("orderno")
        print(f"Your {orderno} is on the way")
        dispatcher.utter_message("Your order {order} was bit late delivary. please wait...")
        



