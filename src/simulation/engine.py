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




def create_agents(NumAgents, StateSpace):
    agents = []
    for i in range(NumAgents):
        loc = (np.random.randint(0, StateSpace), np.random.randint(0, StateSpace))
        ag = agent.Agent(id=i, name=f"Agent_{i}", age=np.random.randint(1, 100), location=loc, health="healthy")
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

    # Rebuild the grid state each step
    grid.clear()
    for idx, hosp in enumerate(hospitals):
        x, y = hosp.location
        grid.addHospital(x, y, idx)
    for ag in agents:
        x, y = ag.location
        grid.addAgent(x, y, ag.id)
