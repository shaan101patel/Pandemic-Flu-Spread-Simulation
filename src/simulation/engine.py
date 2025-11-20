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
