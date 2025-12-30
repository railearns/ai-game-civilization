import random
from dataclasses import dataclass, field
from typing import Dict, List, Any

from .agents import Agent
from .tech import TechTree, Technology
from .events import EventTimeline


@dataclass
class Tribe:
    id: int
    name: str
    resources: Dict[str, float] = field(default_factory=lambda: {"food": 20.0, "wood": 5.0})
    knowledge_pool: float = 0.0
    discovered_tech: Dict[str, bool] = field(default_factory=dict)
    attitude: Dict[int, float] = field(default_factory=dict)  # other_tribe_id -> -1.0..1.0


@dataclass
class Weather:
    name: str
    food_modifier: float


class World:
    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.tick: int = 0
        self.agents: List[Agent] = []
        self.tribes: Dict[int, Tribe] = {}
        self.weather: Weather = Weather("Clear", food_modifier=1.0)
        self.tech_tree = TechTree()
        self.timeline = EventTimeline()

        self._init_tech_tree()
        self._init_tribes_and_agents()

    def _init_tech_tree(self) -> None:
        self.tech_tree.add_technology(Technology(
            id="fire",
            name="Fire",
            description="Basic control of fire; improves survival.",
            prerequisites=[],
            cost_knowledge=5.0,
        ))
        self.tech_tree.add_technology(Technology(
            id="farming",
            name="Farming",
            description="Growing basic crops; more stable food.",
            prerequisites=["fire"],
            cost_knowledge=12.0,
        ))
        self.tech_tree.add_technology(Technology(
            id="writing",
            name="Writing",
            description="Record knowledge; boosts future research speed.",
            prerequisites=["fire"],
            cost_knowledge=15.0,
        ))

    def _init_tribes_and_agents(self) -> None:
        # Two simple tribes to start
        for tribe_id, name in [(1, "Aurora Clan"), (2, "Dusk Wanderers")]:
            tribe = Tribe(id=tribe_id, name=name)
            # Neutral attitude to others
            for other_id in [1, 2]:
                if other_id != tribe_id:
                    tribe.attitude[other_id] = 0.0
            self.tribes[tribe_id] = tribe

        # Spawn agents
        agent_id = 1
        for tribe_id in self.tribes:
            for i in range(5):
                agent = Agent(
                    id=agent_id,
                    name=f"Agent_{agent_id}",
                    tribe_id=tribe_id,
                    aggression=random.uniform(0.1, 0.9),
                    curiosity=random.uniform(0.2, 0.9),
                    cooperativeness=random.uniform(0.2, 0.9),
                )
                self.agents.append(agent)
                agent_id += 1

        self.timeline.add(self.tick, "World created. Two tribes emerge: Aurora Clan and Dusk Wanderers.")

    def _update_weather(self) -> None:
        roll = random.random()
        if roll < 0.7:
            self.weather = Weather("Clear", food_modifier=1.0)
        elif roll < 0.85:
            self.weather = Weather("Rain", food_modifier=1.2)
        else:
            self.weather = Weather("Drought", food_modifier=0.5)

    def _handle_agent_action(self, agent: Agent) -> None:
        action = agent.decide_action()
        tribe = self.tribes[agent.tribe_id]

        if action == "forage":
            base_food = random.uniform(0.5, 2.0) * self.weather.food_modifier
            tribe.resources["food"] += base_food
            agent.hunger = max(0.0, agent.hunger - 0.4)
            agent.remember(self.tick, f"Foraged and brought back {base_food:.1f} food.")
        elif action == "rest":
            agent.fatigue = max(0.0, agent.fatigue - 0.5)
            agent.remember(self.tick, "Rested to recover energy.")
        elif action == "explore":
            # Exploration gives knowledge, maybe events later
            gained_knowledge = random.uniform(0.1, 0.5)
            tribe.knowledge_pool += gained_knowledge
            agent.remember(self.tick, f"Explored the area and gained {gained_knowledge:.2f} knowledge.")
        elif action == "work_for_tribe":
            # Contribute to resources or knowledge, based on personality
            if agent.curiosity > agent.cooperativeness:
                gained_knowledge = random.uniform(0.2, 0.6)
                tribe.knowledge_pool += gained_knowledge
                agent.remember(self.tick, f"Researched and gained {gained_knowledge:.2f} knowledge for the tribe.")
            else:
                gained_food = random.uniform(0.5, 1.5)
                tribe.resources["food"] += gained_food
                agent.remember(self.tick, f"Worked for tribe and added {gained_food:.1f} food.")
        elif action == "idle":
            agent.remember(self.tick, "Idled and observed the surroundings.")

    def _consume_food(self) -> None:
        for tribe in self.tribes.values():
            # Each living agent in tribe consumes food
            members = [a for a in self.agents if a.tribe_id == tribe.id and a.alive]
            demand = 0.3 * len(members)
            if tribe.resources["food"] >= demand:
                tribe.resources["food"] -= demand
            else:
                # Not enough food → agents get hungrier
                for a in members:
                    a.hunger = min(1.0, a.hunger + 0.2)

    def _research_tech(self) -> None:
        for tribe in self.tribes.values():
            candidates = self.tech_tree.available_to_research(tribe.discovered_tech, tribe.knowledge_pool)
            if not candidates:
                continue

            # Pick one to research (later: bias by personality / needs)
            tech = random.choice(candidates)

            tribe.knowledge_pool -= tech.cost_knowledge
            tribe.discovered_tech[tech.id] = True
            self.timeline.add(self.tick, f"{tribe.name} discovered {tech.name}!")
            # Simple tech effect example
            if tech.id == "fire":
                tribe.resources["food"] += 5.0
            if tech.id == "farming":
                tribe.resources["food"] += 10.0

    def _diplomacy_step(self) -> None:
        """Very simple diplomacy: attitudes drift randomly."""
        tribe_ids = list(self.tribes.keys())
        if len(tribe_ids) < 2:
            return

        t1, t2 = random.sample(tribe_ids, 2)
        tribe_a = self.tribes[t1]
        tribe_b = self.tribes[t2]

        delta = random.uniform(-0.05, 0.05)
        tribe_a.attitude[t2] = max(-1.0, min(1.0, tribe_a.attitude.get(t2, 0.0) + delta))
        tribe_b.attitude[t1] = max(-1.0, min(1.0, tribe_b.attitude.get(t1, 0.0) + delta))

        # Optional: log major changes
        if tribe_a.attitude[t2] > 0.7:
            self.timeline.add(self.tick, f"{tribe_a.name} and {tribe_b.name} are close allies.")
        if tribe_a.attitude[t2] < -0.7:
            self.timeline.add(self.tick, f"Tension rises between {tribe_a.name} and {tribe_b.name}.")

    def tick_world(self) -> None:
        self.tick += 1
        self._update_weather()

        # Agent-level updates
        for agent in self.agents:
            agent.tick_needs()
            if agent.alive:
                self._handle_agent_action(agent)

        # Tribe-level updates
        self._consume_food()
        self._research_tech()
        self._diplomacy_step()

        # Global events example
        if self.tick % 20 == 0:
            self.timeline.add(self.tick, f"Year {self.tick // 20} has passed under {self.weather.name} skies.")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tick": self.tick,
            "weather": {
                "name": self.weather.name,
                "food_modifier": self.weather.food_modifier,
            },
            "tribes": [
                {
                    "id": t.id,
                    "name": t.name,
                    "resources": t.resources,
                    "knowledge_pool": t.knowledge_pool,
                    "discovered_tech": list(t.discovered_tech.keys()),
                    "attitude": t.attitude,
                }
                for t in self.tribes.values()
            ],
            "agents": [a.to_dict() for a in self.agents],
            "timeline": self.timeline.to_list(),
        }
