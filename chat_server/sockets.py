import asyncio
import websockets
import abc
import json
import uuid
from enums import ClientTypes
import pytest


@pytest.mark.skip
class ISocketServer(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    async def main(self, websocket, path):
        pass

    @abc.abstractmethod
    def setup(self):
        pass

    @abc.abstractmethod
    def run(self):
        pass


@pytest.mark.skip
class AbstractSocketServer(ISocketServer):  # pragma: no cover
    def __init__(self):
        self.server = None

    @abc.abstractmethod
    async def main(self, websocket, path):
        pass

    def setup(self):
        self.server = websockets.serve(self.main, "localhost", 3000)
        return self

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()


class ClientConnection:
    def __init__(self, connection=None, id=None, type=None, chat=None):
        self.connection = connection
        self.id = id
        self.type = type
        self.chat = chat


class ChatServer(AbstractSocketServer):

    def __init__(self):
        super().__init__()
        self.clients = []

    def get_lazy_support(self):
        supports = list(
            filter(lambda client: client.type == ClientTypes.SUPPORT.value and client.chat is None, self.clients))

        if not len(supports):
            return None

        return supports[0]

    def get_lazy_customer(self):
        customers = list(
            filter(lambda client: client.type == ClientTypes.CUSTOMER.value and client.chat is None, self.clients))

        if not len(customers):
            return None

        return customers[0]

    @pytest.mark.skip(reason="async methods will be tested in the future")
    async def connect_customer_to_support(self):  # pragma: no cover
        support = self.get_lazy_support()
        customer = self.get_lazy_customer()

        if support is None or customer is None:
            return None

        support.chat = customer
        customer.chat = support

        await support.connection.send(json.dumps({"text": "Você está connectado a um cliente"}))
        await customer.connection.send(json.dumps({"text": "Você está connectado a um assistente"}))

        return True

    @pytest.mark.skip(reason="async methods will be tested in the future")
    async def setup_support(self, origin):  # pragma: no cover
        origin.type = ClientTypes.SUPPORT.value
        self.clients.append(origin)

        await origin.connection.send(json.dumps({"text": "Você está connectado"}))
        await self.connect_customer_to_support()

    @pytest.mark.skip(reason="async methods will be tested in the future")
    async def setup_customer(self, origin):  # pragma: no cover
        origin.type = ClientTypes.CUSTOMER.value
        self.clients.append(origin)

        await self.connect_customer_to_support()

    @classmethod
    @pytest.mark.skip(reason="async methods will be tested in the future")
    async def send_message(cls, connection, message):  # pragma: no cover
        if connection.chat is not None:
            await connection.chat.connection.send(json.dumps({"text": message}))

    @pytest.mark.skip(reason="async methods will be tested in the future")
    async def manage_message(self, message):  # pragma: no cover
        if message["data"]["action"] == "new_customer":
            await self.setup_customer(message["origin"])

        elif message["data"]["action"] == "new_support":
            await self.setup_support(message["origin"])

        elif message["data"]["action"] == "new_message":
            await self.send_message(message["origin"], message["data"]["message"])

    @pytest.mark.skip(reason="async methods will be tested in the future")
    async def new_message(self, message, origin):  # pragma: no cover
        data = {
            "origin": origin,
            "data": message
        }

        await self.manage_message(data)

    @pytest.mark.skip(reason="async methods will be tested in the future")
    async def main(self, websocket, path):  # pragma: no cover
        client = ClientConnection(websocket, uuid.uuid4().hex)

        while True:
            try:
                data = await client.connection.recv()
                await self.new_message(json.loads(data), client)
            except websockets.exceptions.ConnectionClosedOK:
                for cl in self.clients:
                    if cl.chat is not None and client.id == cl.chat.id:
                        cl.chat = None

                self.clients.remove(client)

                await self.connect_customer_to_support()
                break
            except Exception:
                await client.connection.send(json.dumps({"text": 'Ocorreu um erro interno.'}))
