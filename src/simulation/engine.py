import numpy as np

import models.agent as agent
import models.hospital as hospital


def create_hospitals(NumOfHospitals, StateSpace):
    hospitals = []
    for i in range(NumOfHospitals):
        x = np.random.randint(0, StateSpace)
        y = np.random.randint(0, StateSpace)
        vaccine_type = "A" if i % 2 == 0 else "B"
        hosp = hospital.Hospital(location=(x, y), vaccine_capacity=1000, vaccine_type=vaccine_type, admin_speed=10)
        hospitals.append(hosp)
    return hospitals




def create_agents(NumAgents, StateSpace, NumSick=0):
    agents = []
    for i in range(NumAgents):
        loc = (np.random.randint(0, StateSpace), np.random.randint(0, StateSpace))
                
        # Sampled da age from normal distribution (mean=40, std=20), clipped to [0, 90]
        age = int(np.clip(np.random.normal(40, 20), 0, 90))
        
        health = "healthy"
        if i < NumSick:
            health = "infected"
            
        ag = agent.Agent(id=i, name=f"Agent_{i}", age=age, location=loc, health=health)
        agents.append(ag)
    return agents


def step(agents, hospitals, grid, StateSpace):
    # Moves each agent one step to a random neighboring cell (including staying put),
    # then rebuilds the grid occupancy accordingly.
    for ag in agents:
        x, y = ag.location
        dx = int(np.random.choice([-1, 0, 1]))
        dy = int(np.random.choice([-1, 0, 1]))
        nx = max(0, min(StateSpace - 1, x + dx))
        ny = max(0, min(StateSpace - 1, y + dy))
        ag.move((nx, ny))

    # --- Disease Transmission Logic ---
    # Group agents by location
    location_agents = {}
    for ag in agents:
        loc = ag.location
        if loc not in location_agents:
            location_agents[loc] = []
        location_agents[loc].append(ag)

    # Check transmission within each cell
    for loc, cell_agents in location_agents.items():
        # Check if there is at least one sick person (infected or infectious)
        if any(a.health in ["infected", "infectious"] for a in cell_agents):
            for a in cell_agents:
                if a.health == "healthy":
                    # Sample from normal distribution
                    val = np.random.normal(50, 15)
                    if val > 50:
                        a.updateHealth("infected")
                        a.days_infected = 0

    # --- Disease Progression Logic ---
    for ag in agents:
        if ag.health == "infected":
            ag.days_infected += 1
            if ag.days_infected > 5:
                ag.updateHealth("infectious")

    # Rebuild the grid state each step
    grid.clear()
    for idx, hosp in enumerate(hospitals):
        x, y = hosp.location
        grid.addHospital(x, y, idx)
    for ag in agents:
        x, y = ag.location
        grid.addAgent(x, y, ag.id)
