from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionSimulateLoan(Action):
    @classmethod
    def get_credit(cls, income: float) -> dict:
        response = {
            "credit": 0,
            "installment": 0
        }

        if income < 1000:
            return None

        if 1000 <= income < 5000:
            response["credit"] = 10000.00
            response["installment"] = 24
        elif income >= 5000:
            response["credit"] = 20000.00
            response["installment"] = 30

        return response

    def name(self) -> Text:
        return "action_simulate_loan"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        result = self.get_credit(float(tracker.get_slot("income")))

        if result is None:
            dispatcher.utter_message(message_template="utter_no_pre_approved_credit")
            return []

        message = """{}, conforme nossos critérios você teria um crédito pré-aprovado de {}, podendo ser 
        parcelado em até {} vezes.\n""".format(tracker.get_slot("name"), result["credit"], result["installment"])

        dispatcher.utter_message(message)

        return []


class ActionTransferToHuman(Action):
    def name(self) -> Text:
        return "action_transfer_to_human"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        config = {
            "host": '127.0.0.1:3000'
        }

        dispatcher.utter_message(json_message=config)

        return []
