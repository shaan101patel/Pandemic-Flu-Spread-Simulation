class Grid:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[0 for _ in range(width)] for _ in range(height)]

    def set_cell(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x] = value
        else:
            raise IndexError("Cell position out of bounds")

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        else:
            raise IndexError("Cell position out of bounds")

    def __str__(self):
        grid_str = ""
        for row in self.cells:
            grid_str += " ".join(str(cell) for cell in row) + "\n"
        return grid_str
    
    def clear(self):
        self.cells = [["" for _ in range(self.width)] for _ in range(self.height)]

    def addHospital(self, x, y, hospital_id):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x] = f"H{hospital_id}"
        else:
            raise IndexError("Cell position out of bounds")

    # No two agents can occupy the same cell 
    def addAgent(self, x, y, agent_id):
        if 0 <= x < self.width and 0 <= y < self.height:
            current_value = self.cells[y][x]
            if current_value == 0:
                self.cells[y][x] = f"A{agent_id}"
            else:
                self.cells[y][x] = f"{current_value},A{agent_id}"
        else:
            raise IndexError("Cell position out of bounds")