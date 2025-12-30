from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Technology:
    id: str
    name: str
    description: str
    prerequisites: List[str]
    cost_knowledge: float


@dataclass
class TechTree:
    technologies: Dict[str, Technology] = field(default_factory=dict)

    def add_technology(self, tech: Technology) -> None:
        self.technologies[tech.id] = tech

    def available_to_research(self, discovered: Dict[str, bool], knowledge_pool: float) -> List[Technology]:
        result = []
        for tech in self.technologies.values():
            if discovered.get(tech.id, False):
                continue
            if any(not discovered.get(pre, False) for pre in tech.prerequisites):
                continue
            if knowledge_pool >= tech.cost_knowledge:
                result.append(tech)
        return result
