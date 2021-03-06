from rasa_sdk.executor import CollectingDispatcher
from ..actions import ActionSimulateLoan, ActionTransferToHuman

class FakeDomain:
    def __init__(self):
        pass


class FakeTracker:
    def get_slot(self, slot):
        pass


class ActionSimulateLoanTest:
    def setup(self, mocker):
        self.service = ActionSimulateLoan()
        self.dispatcher = CollectingDispatcher()
        self.tracker = FakeTracker()
        self.domain = FakeDomain()

        mocker.patch.object(self.dispatcher, "utter_message", return_value=None)

    def test_name_should_return_string(self, mocker):
        self.setup(mocker)
        assert self.service.name() == "action_simulate_loan"

    def test_get_credit_should_utter_no_pre_approved_credit(self, mocker):
        self.setup(mocker)
        mocker.patch.object(self.tracker, "get_slot", return_value=100)

        assert self.service.run(self.dispatcher, self.tracker, self.domain) == []

    def test_get_credit_should_grant_10000_in_credit(self, mocker):
        self.setup(mocker)
        mocker.patch.object(self.tracker, "get_slot", return_value=4999)

        assert self.service.run(self.dispatcher, self.tracker, self.domain) == []

    def test_get_credit_should_grant_20000_in_credit(self, mocker):
        self.setup(mocker)
        mocker.patch.object(self.tracker, "get_slot", return_value=6000)

        assert self.service.run(self.dispatcher, self.tracker, self.domain) == []


def test_ActionSimulateLoan(mocker):
    ActionSimulateLoanTest().test_name_should_return_string(mocker)
    ActionSimulateLoanTest().test_get_credit_should_utter_no_pre_approved_credit(mocker)
    ActionSimulateLoanTest().test_get_credit_should_grant_10000_in_credit(mocker)
    ActionSimulateLoanTest().test_get_credit_should_grant_20000_in_credit(mocker)

class ActionTransferToHumanTest:
    def setup(self, mocker):
        self.service = ActionTransferToHuman()
        self.dispatcher = CollectingDispatcher()
        self.tracker = FakeTracker()
        self.domain = FakeDomain()

        mocker.patch.object(self.dispatcher, "utter_message", return_value=None)

    def test_name_should_return_string(self, mocker):
        self.setup(mocker)
        assert self.service.name() == "action_transfer_to_human"

    def test_should_utter_json_and_return_empty_list(self, mocker):
        self.setup(mocker)

        assert self.service.run(self.dispatcher, self.tracker, self.domain) == []


def test_ActionTransferToHuman(mocker):
    ActionTransferToHumanTest().test_name_should_return_string(mocker)
    ActionTransferToHumanTest().test_should_utter_json_and_return_empty_list(mocker)
