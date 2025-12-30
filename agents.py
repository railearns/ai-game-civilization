import random
from typing import List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class MemoryEvent:
    tick: int
    description: str


@dataclass
class Agent:
    id: int
    name: str
    tribe_id: int
    # Basic personality traits: 0.0–1.0
    aggression: float
    curiosity: float
    cooperativeness: float

    hunger: float = 0.0   # 0.0–1.0
    fatigue: float = 0.0  # 0.0–1.0
    happiness: float = 0.5

    knowledge: Dict[str, float] = field(default_factory=dict)
    memory: List[MemoryEvent] = field(default_factory=list)

    alive: bool = True

    def tick_needs(self) -> None:
        """Update basic needs over time."""
        if not self.alive:
            return

        self.hunger = min(1.0, self.hunger + 0.05)
        self.fatigue = min(1.0, self.fatigue + 0.03)

        # Happiness goes down if needs are bad
        self.happiness -= 0.02 * (self.hunger + self.fatigue)
        self.happiness = max(0.0, min(1.0, self.happiness))

        # Simple death condition
        if self.hunger >= 1.0 and self.fatigue >= 1.0:
            self.alive = False

    def remember(self, tick: int, description: str) -> None:
        if len(self.memory) > 32:
            self.memory.pop(0)
        self.memory.append(MemoryEvent(tick, description))

    def decide_action(self) -> str:
        """Very simple behavior based on needs and personality."""
        if not self.alive:
            return "dead"

        if self.hunger > 0.7:
            return "forage"
        if self.fatigue > 0.8:
            return "rest"

        # Higher curiosity → more exploration
        if random.random() < self.curiosity:
            return "explore"

        # Cooperative agents may try to help tribe
        if random.random() < self.cooperativeness:
            return "work_for_tribe"

        return "idle"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "tribe_id": self.tribe_id,
            "aggression": self.aggression,
            "curiosity": self.curiosity,
            "cooperativeness": self.cooperativeness,
            "hunger": self.hunger,
            "fatigue": self.fatigue,
            "happiness": self.happiness,
            "alive": self.alive,
        }
