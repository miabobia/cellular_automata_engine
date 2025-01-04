from typing import Any, Callable
from dataclasses import dataclass

@dataclass
class Event:
    name: str
    data: Any

class EventDispatch:

    listeners = {}

    def add_listener(self, name: str, listener: Callable) -> None:
        if name not in self.listeners:
            self.listeners[name] = []
        self.listeners[name].append(listener)
    
    def dispatch(self, event: str) -> None:
        if event.name not in self.listeners: return
        for listener in self.listeners[event.name]:
            listener(event)