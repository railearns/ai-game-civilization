🧠 AI Civilization Simulator
A procedural society simulation where autonomous agents evolve cultures, technologies, and relationships over time. Inspired by Dwarf Fortress, RimWorld, and Spore — but built from scratch in Python + HTML/JS.

🚀 Features
Agents with needs, personalities, and memory

Procedural weather and resource simulation

Technology tree with dynamic discovery

Tribe-level diplomacy and attitude shifts

Timeline of major world events

Real-time web viewer (HTML + JS)

🛠 Tech Stack
Python 3 (simulation engine)

HTML/CSS/JavaScript (viewer)

JSON (state sync between backend and frontend)

▶️ How to Run
1. Start the simulation
bash
python -m simulation.main
2. Serve the viewer
bash
python -m http.server 8000
3. Open in browser
Code
http://localhost:8000/web/index.html
📁 Folder Structure
Code
ai_civilization/
├── simulation/   # Python backend
├── web/          # HTML/JS viewer
├── state.json    # Live simulation output
💡 Next Ideas
Procedural language generation

Cultural traits and rituals

War, alliances, and diplomacy

Save/load system

Unity or Godot port
