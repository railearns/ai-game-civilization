import json
import time

from .world import World


def run_simulation(steps: int = 100, write_every: int = 5) -> None:
    world = World(seed=123)

    for i in range(steps):
        world.tick_world()

        if world.tick % write_every == 0:
            state = world.to_dict()
            with open("state.json", "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
            print(f"[tick {world.tick}] State written to state.json")

        # Slow down a little so you can watch it evolve
        time.sleep(0.1)


if __name__ == "__main__":
    run_simulation(steps=200, write_every=5)
