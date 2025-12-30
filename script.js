async function fetchState() {
  try {
    const response = await fetch('../state.json?_=' + Date.now());
    if (!response.ok) {
      throw new Error('Failed to load state.json');
    }
    const data = await response.json();
    renderState(data);
  } catch (err) {
    console.error(err);
  }
}

function renderState(state) {
  document.getElementById('tick').textContent = state.tick;
  document.getElementById('weather').textContent = `${state.weather.name} (x${state.weather.food_modifier})`;

  renderTribes(state.tribes);
  renderAgents(state.agents);
  renderTimeline(state.timeline);
}

function renderTribes(tribes) {
  const container = document.getElementById('tribes');
  container.innerHTML = '';

  tribes.forEach((tribe) => {
    const div = document.createElement('div');
    div.className = 'tribe';

    const techList = tribe.discovered_tech.length
      ? tribe.discovered_tech.join(', ')
      : 'None';

    div.innerHTML = `
      <h3>${tribe.name}</h3>
      <p><strong>ID:</strong> ${tribe.id}</p>
      <p><strong>Resources:</strong> food=${tribe.resources.food.toFixed(1)}, wood=${tribe.resources.wood.toFixed(1)}</p>
      <p><strong>Knowledge pool:</strong> ${tribe.knowledge_pool.toFixed(2)}</p>
      <p><strong>Tech:</strong> ${techList}</p>
    `;
    container.appendChild(div);
  });
}

function renderAgents(agents) {
  const container = document.getElementById('agents');
  container.innerHTML = '';

  agents.forEach((a) => {
    const div = document.createElement('div');
    div.className = 'agent';
    div.innerHTML = `
      <p>
        <strong>${a.name}</strong>
        [tribe ${a.tribe_id}] - 
        alive: ${a.alive} |
        hunger: ${a.hunger.toFixed(2)} |
        fatigue: ${a.fatigue.toFixed(2)} |
        happiness: ${a.happiness.toFixed(2)}
      </p>
    `;
    container.appendChild(div);
  });
}

function renderTimeline(events) {
  const container = document.getElementById('timeline');
  container.innerHTML = '';

  events.slice().reverse().forEach((e) => {
    const div = document.createElement('div');
    div.className = 'timeline-item';
    div.textContent = `[${e.tick}] ${e.description}`;
    container.appendChild(div);
  });
}

// Refresh every second
setInterval(fetchState, 1000);
fetchState();
