import asyncio

from PIL import Image


class Operator:
    def __init__(self, loop: asyncio.base_events.BaseEventLoop = None) -> None:
        self.__loop = loop or asyncio.get_event_loop()
