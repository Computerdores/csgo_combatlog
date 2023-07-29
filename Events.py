from typing import Callable
from typing_extensions import Protocol

class EventCallback(Protocol):
    async def __call__(self, __event_group: int, __event_id: int, __old_value, __new_value):
        pass

class EventSystem:
    def __init__(self):
        self._queue = []
        self._listeners = []
    
    def queue_event(self, event_group: int, event_id: int, old_value, new_value):
        self._queue.append((event_group, event_id, old_value, new_value))

    async def process_events(self):
        for e_g, e_id, o_v, n_v in self._queue:
            for ce_g, ce_id, c in self._listeners:
                if ce_g == None or (ce_g == e_g and (ce_id == None or ce_id == e_id)):
                    c(e_g, e_id, o_v, n_v)

    def add_listener(self, event_group: int, event_id: int, listener: EventCallback):
        self._listeners.append((event_group, event_id, listener))
