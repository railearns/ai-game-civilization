from dataclasses import dataclass
from typing import List


@dataclass
class WorldEvent:
    tick: int
    description: str


class EventTimeline:
    def __init__(self, max_events: int = 200):
        self.max_events = max_events
        self.events: List[WorldEvent] = []

    def add(self, tick: int, description: str) -> None:
        if len(self.events) >= self.max_events:
            self.events.pop(0)
        self.events.append(WorldEvent(tick, description))

    def to_list(self) -> List[dict]:
        return [{"tick": e.tick, "description": e.description} for e in self.events]
