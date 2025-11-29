
class Agent:

    def __init__(self, id: int, name: str, age: int, location: tuple, health: str, mask: bool = False):

        # traits
        self.id = id
        self.name = name
        self.age = age
        self.location = location
        self.health = health
        self.mask = mask
        self.days_infected = 0
        self.vaccine_doses = 0
        self.received_vaccine_types = set()
        self.immunity_reason = None # "vaccine", "natural", "treatment"


    def get_info(self) -> str:
        return f"Agent ID: {self.id}, Name: {self.name}, Age: {self.age}, Location: {self.location}, Health: {self.health}, Doses: {self.vaccine_doses}, Vaccine Types: {list(self.received_vaccine_types)}, Immunity Reason: {self.immunity_reason}"
    
    def move(self, new_location: tuple):
        self.location = new_location

    def updateHealth(self, new_health: str):
        self.health = new_health

    def healthStatus(self) -> str:
        return self.health
    
    def putOnMask(self):
        self.mask = True
    
    def maskStatus(self) -> bool:
        return self.mask
