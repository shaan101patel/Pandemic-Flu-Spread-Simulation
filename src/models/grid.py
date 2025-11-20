class Grid:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[[] for _ in range(width)] for _ in range(height)]

    def set_cell(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x] = [value]
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
            # Display cell contents separated by commas, or empty space if empty
            row_content = []
            for cell in row:
                if cell:
                    row_content.append(",".join(str(item) for item in cell))
                else:
                    row_content.append(".")
            grid_str += " | ".join(row_content) + "\n"
        return grid_str
    
    def clear(self):
        self.cells = [[[] for _ in range(self.width)] for _ in range(self.height)]

    def addHospital(self, x, y, hospital_id):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x].append(f"H{hospital_id}")
        else:
            raise IndexError("Cell position out of bounds")

    # Agents can occupy the same cell 
    def addAgent(self, x, y, agent_id):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[y][x].append(f"A{agent_id}")
        else:
            raise IndexError("Cell position out of bounds")