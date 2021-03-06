import asyncio
import websockets
import abc
import json
import uuid
from enums import ClientTypes


class ISocketServer(abc.ABC):
    @abc.abstractmethod
    async def main(self, websocket, path):
        pass

    @abc.abstractmethod
    def setup(self):
        pass

    @abc.abstractmethod
    def run(self):
        pass


class AbstractSocketServer(ISocketServer):
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
    def __init__(self, connection, id):
        self.connection = connection
        self.id = id
        self.type = None
        self.chat = None


class ChatServer(AbstractSocketServer):

    def __init__(self):
        super().__init__()
        self.clients = []

    def get_lazy_supporter(self):
        supporters = list(
            filter(lambda client: client.type == ClientTypes.SUPPORT.value and client.chat is None, self.clients))

        if not len(supporters):
            return None

        return supporters[0]

    def get_lazy_customer(self):
        customers = list(
            filter(lambda client: client.type == ClientTypes.CUSTOMER.value and client.chat is None, self.clients))

        if not len(customers):
            return None

        return customers[0]

    async def connect_customer_to_supporter(self):
        supporter = self.get_lazy_supporter()
        customer = self.get_lazy_customer()

        if supporter is None or customer is None:
            return None

        supporter.chat=customer
        customer.chat=supporter

        await supporter.connection.send(json.dumps({"text": "Você está connectado a um cliente"}))
        await customer.connection.send(json.dumps({"text": "Você está connectado a um assistente"}))

        return True

    async def setup_supporter(self, origin):
        origin.type = ClientTypes.SUPPORT.value
        self.clients.append(origin)

        await origin.connection.send(json.dumps({"text": "Você está connectado"}))
        await self.connect_customer_to_supporter()

    async def setup_customer(self, origin):
        origin.type = ClientTypes.CUSTOMER.value
        self.clients.append(origin)

        await self.connect_customer_to_supporter()

    @classmethod
    async def send_message(cls, connection, message):
        if connection.chat is not None:
            await connection.chat.connection.send(json.dumps({"text": message}))

    async def manage_message(self, message):
        if message["data"]["action"] == "new_customer":
            await self.setup_customer(message["origin"])

        elif message["data"]["action"] == "new_supporter":
            await self.setup_supporter(message["origin"])

        elif message["data"]["action"] == "new_message":
            await self.send_message(message["origin"], message["data"]["message"])

    async def new_message(self, message, origin):
        data = {
            "origin": origin,
            "data": message
        }

        await self.manage_message(data)

    async def main(self, websocket, path):
        client = ClientConnection(websocket, uuid.uuid4().hex)

        while True:
            try:
                data = await client.connection.recv()
                await self.new_message(json.loads(data), client)
            except websockets.exceptions.ConnectionClosedOK:
                for cl in self.clients:
                    if client.id == cl.chat.id:
                        cl.chat = None

                self.clients.remove(client)
                break
            except Exception as e:
                await client.connection.send(json.dumps({"text": 'Ocorreu um erro interno.'}))
