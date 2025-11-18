import numpy as np

import models.agent as agent
import models.hospital as hospital


def create_hospitals(NumOfHospitals, StateSpace):
    hospitals = []
    # spacing ensures hospitals are placed within the StateSpace bounds
    spacing = max(1, StateSpace // max(1, NumOfHospitals))
    for i in range(NumOfHospitals):
        for j in range(NumOfHospitals):
            x = min(i * spacing, StateSpace - 1)
            y = min(j * spacing, StateSpace - 1)
            hosp = hospital.Hospital(location=(x, y), vaccine_capacity=1000, vaccine_type="A", admin_speed=10)
            hospitals.append(hosp)
    return hospitals




def create_agents(NumAgents, StateSpace):
    agents = []
    for i in range(NumAgents):
        loc = (np.random.randint(0, StateSpace), np.random.randint(0, StateSpace))
        ag = agent.Agent(id=i, name=f"Agent_{i}", age=np.random.randint(1, 100), location=loc, health="healthy")
        agents.append(ag)
    return agents
