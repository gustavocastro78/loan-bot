from ..sockets import ChatServer, ClientConnection


class FakeDomain:
    def __init__(self):
        pass


class FakeTracker:
    def get_slot(self, slot):
        pass


class ChatServerTest:
    def setup(self, mocker):
        self.server = ChatServer()
        self.clientConnection = ClientConnection()

    def test_get_lazy_support_should_return_connection(self, mocker):
        self.setup(mocker)

        self.clientConnection.id = 123
        self.clientConnection.type = 0
        self.server.clients.append(self.clientConnection)

        assert type(self.server.get_lazy_support()) == ClientConnection

    def test_get_lazy_support_should_return_None(self, mocker):
        self.setup(mocker)

        self.server.clients.append(self.clientConnection)

        assert self.server.get_lazy_support() is None

    def test_get_lazy_customer_should_return_connection(self, mocker):
        self.setup(mocker)

        self.clientConnection.id = 123
        self.clientConnection.type = 1
        self.server.clients.append(self.clientConnection)

        assert type(self.server.get_lazy_customer()) == ClientConnection

    def test_get_lazy_customer_should_return_None(self, mocker):
        self.setup(mocker)

        self.server.clients.append(self.clientConnection)

        assert self.server.get_lazy_customer() is None

    # @pytest.mark.asyncio
    # async def test_connect_customer_to_support_should_return_None(self, mocker):
    #     self.setup(mocker)
    #     self.server.clients.append(self.clientConnection)
    #
    #     mocker.patch.object(self.server, "get_lazy_customer", return_value=None)
    #     mocker.patch.object(self.server, "get_lazy_support", return_value=None)
    #
    #     assert await self.server.connect_customer_to_support() is None


async def test_ActionSimulateLoan(mocker):
    ChatServerTest().test_get_lazy_support_should_return_connection(mocker)
    ChatServerTest().test_get_lazy_support_should_return_None(mocker)
    ChatServerTest().test_get_lazy_customer_should_return_connection(mocker)
    ChatServerTest().test_get_lazy_customer_should_return_None(mocker)
    # await ChatServerTest().test_connect_customer_to_support_should_return_None(mocker)

