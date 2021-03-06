import enum


class SocketActions(enum.Enum):
    START_CONNECTION = 0
    CLOSE_CONNECTION = 1
    RECEIVE_MESSAGE = 2
    SEND_MESSAGE = 3


class ClientTypes(enum.Enum):
    SUPPORT = 0
    CUSTOMER = 1
