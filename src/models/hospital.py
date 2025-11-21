class Hospital:

    def __init__(self, location: tuple, vaccine_capacity: int, vaccine_type: str, admin_speed: int, bed_capacity: float):
        self.location = location
        self.vaccine_capacity = vaccine_capacity
        self.vaccine_type = vaccine_type
        self.admin_speed = admin_speed
        self.bed_capacity = bed_capacity
        self.current_patients = 0
        self.active = True


    def get_info(self) -> str:
        return f"Hospital Location: {self.location}, Vaccine Capacity: {self.vaccine_capacity}, Vaccine Type: {self.vaccine_type}, Bed Capacity: {self.bed_capacity}, Active: {self.active}"
    
    def administer_vaccine(self, number_of_doses: int) -> bool:
        if self.active and number_of_doses <= self.vaccine_capacity:
            self.vaccine_capacity -= number_of_doses
            return True
        else:
            return False
        
    def update_occupancy(self, count: int):
        self.current_patients = count
        if self.current_patients > self.bed_capacity:
            self.active = False
        
    def restock_vaccines(self, additional_doses: int):
        self.vaccine_capacity += additional_doses

    def location(self, location: tuple):
        return tuple

    def is_active(self) -> bool:
        return self.active
    
    def deactivate(self):
        self.active = False


