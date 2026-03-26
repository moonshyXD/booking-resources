from typing import Callable, Awaitable, Dict, Any


class EventDispatcher:
    def __init__(self):
        self._routes: Dict[str, Callable[[Dict[str, Any]], Awaitable[None]]] = {}

    def register(self, event_name: str, handler: Callable[[Dict[str, Any]], Awaitable[None]]):
        self._routes[event_name] = handler

    async def handle(self, event_name: str, payload: dict):
        handler = self._routes.get(event_name)
        if not handler:
            return None

        return await handler(payload)