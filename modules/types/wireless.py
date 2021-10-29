# wireless module template and supporting classes

from abc import ABCMeta, abstractmethod

class Regions: 
    america = 0
    europe = 1

class Modes:
    transmit = 0
    recieve = 1

# Lora Exceptions
class WrongModeException(Exception):
    pass

class NotConnectedException(Exception):
    pass

class WirelessModule:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, port, rate, region, mode, callback) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_data(self, data) -> None:
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def configure(self, port=None, rate=None, region=None, mode=None, callback=None) -> None:
        raise NotImplementedError
