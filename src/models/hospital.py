class Hospital:

    def __init__(self, location: tuple, vaccine_capacity: int, vaccine_type: str, admin_speed: int):
        self.location = location
        self.vaccine_capacity = vaccine_capacity
        self.vaccine_type = vaccine_type
        self.admin_speed = admin_speed

    def get_info(self) -> str:
        return f"Hospital Location: {self.location}, Vaccine Capacity: {self.vaccine_capacity}, Vaccine Type: {self.vaccine_type}"
    
    def administer_vaccine(self, number_of_doses: int) -> bool:
        if number_of_doses <= self.vaccine_capacity:
            self.vaccine_capacity -= number_of_doses
            return True
        else:
            return False
        
    def restock_vaccines(self, additional_doses: int):
        self.vaccine_capacity += additional_doses



