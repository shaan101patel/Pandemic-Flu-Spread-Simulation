import numpy as np

import models.agent as agent
import models.hospital as hospital


def create_hospitals(NumOfHospitals, StateSpace, CityPopulation):
    hospitals = []
    # Ensure at least a minimum capacity for small simulations
    calculated_capacity = (CityPopulation / 1000) * 2.35
    bed_capacity = max(5, int(calculated_capacity))
    
    for i in range(NumOfHospitals):
        x = np.random.randint(0, StateSpace)
        y = np.random.randint(0, StateSpace)
        vaccine_type = "Type 1" if i % 2 == 0 else "Type 2"
        hosp = hospital.Hospital(location=(x, y), vaccine_capacity=10000, vaccine_type=vaccine_type, admin_speed=10000, bed_capacity=bed_capacity  * 100)
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

def randomWalk(agent, StateSpace):
    x, y = agent.location
    dx = int(np.random.choice([-1, 0, 1]))
    dy = int(np.random.choice([-1, 0, 1]))
    nx = max(0, min(StateSpace - 1, x + dx))
    ny = max(0, min(StateSpace - 1, y + dy))
    agent.move((nx, ny))


def findHosp(hospitals, agent, StateSpace):
    
    closestHosp = (hospitals[0], 999999999999999)
    x, y = agent.location
    nx, ny = x, y

    for hosp in hospitals:
        hx, hy = hosp.location
        dist = abs(hx - x) + abs(hy - y)

        if dist < closestHosp[1]:
            closestHosp = (hosp, dist)
    
    # Target the closest hospital
    target_hosp = closestHosp[0]
    hx, hy = target_hosp.location
        
    if x == hx:
        if hy - y > 0:
            ny += 1
        elif hy - y < 0:
            ny -= 1
    else: 
        if hx - x > 0:
            nx += 1
        else:
            nx -= 1

    agent.move((nx, ny))

def get_age_based_params(age):
    if age <= 4:
        return 0.27111401, 1.5623923
    elif age <= 9:
        return 0.27619241, 1.5853057
    elif age <= 17:
        return 0.23507195, 1.35129295
    elif age <= 29:
        return 0.16806533, 1.11063756
    elif age <= 39:
        return 0.17647801, 1.28169089
    elif age <= 49:
        return 0.16738755, 1.14906492
    elif age <= 59:
        return 0.15507585, 1.22311138
    elif age <= 69:
        return 0.16214078, 1.15063113
    elif age <= 79:
        return 0.17056577, 1.17523736
    else:
        return 0.20907177, 1.35574058











# Main simulation step:

def step(agents, hospitals, grid, StateSpace):
    # Moves each agent one step to a random neighboring cell (including staying put),
    # then rebuilds the grid occupancy accordingly.
    
    active_hospitals = [h for h in hospitals if h.active]

    for ag in agents:
        # given that symptoms often appearing around 5-6 days after exposure. and a chance of infected constanlty chaning minds about 50% of the time:
        if ag.healthStatus() != "healthy" and active_hospitals and ag.days_infected >= 6 and np.random.rand() < 0.5: 
            findHosp(active_hospitals, ag, StateSpace)
        else:
            randomWalk(ag, StateSpace)

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
                    # Sample from normal distribution based on age
                    mean, sd = get_age_based_params(a.age)
                    val = np.random.normal(mean, sd)
                    if val > 0:
                        a.updateHealth("infected")
                        a.days_infected = 0

    # --- Disease Progression Logic ---
    for ag in agents:
        if ag.health == "infected":
            ag.days_infected += 1
            if ag.days_infected > 5:
                ag.updateHealth("infectious")

    # --- Hospital Interaction Logic ---
    for hosp in hospitals:
        # Count agents at this hospital's location
        patients_here = [ag for ag in agents if ag.location == hosp.location]
        hosp.update_occupancy(len(patients_here))
        
        if hosp.active:
            for ag in patients_here:
                if ag.health in ["infected", "infectious"]:
                    if hosp.administer_vaccine(1):
                        ag.updateHealth("healthy")
                        ag.days_infected = 0

    # Rebuild the grid state each step
    grid.clear()
    for idx, hosp in enumerate(hospitals):
        x, y = hosp.location
        grid.addHospital(x, y, idx)
    for ag in agents:
        x, y = ag.location
        grid.addAgent(x, y, ag.id)
