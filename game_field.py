from itertools import product

class GameField():
    
    def __init__(self, size):
        self.size = size
        self.solitude_mark = 1
        self.overpopulation_mark = 4
        self.newborn_mark = 3
        self.reset()
        
    def within_field(self, x, y):
        return x >=0 and y >=0 and x < self.size and y < self.size
    
    def get_cell_at(self, x, y):
        return self.matrix[y][x]
    
    def add_cell_at(self, x, y):
        self.add_cell(Cell(x, y))
        
    def remove_cell_at(self, x, y):
        cell = self.matrix[y][x]
        if cell != None:
            self.remove_cell(cell)
        
    def add_cell(self, cell):
        if self.within_field(cell.x, cell.y):
            self.live_cells.append(cell)
            self.matrix[cell.y][cell.x] = cell
        
    def remove_cell(self, cell):
        if cell in self.live_cells:
            self.matrix[cell.y][cell.x] = None
            self.live_cells.remove(cell)
        
    def update(self):
        self.collect_dying_cells()
        self.create_newborn_cells()
        self.remove_dying_cells()
        self.promote_newborn_cells()
        
    def collect_dying_cells(self):
        for cell in self.live_cells:
            siblings = [
                self.get_cell_at(sibling[0], sibling[1]) for sibling in cell.get_sibling_indices() 
                if self.within_field(sibling[0], sibling[1])
                    and self.get_cell_at(sibling[0], sibling[1]) != None
            ]
            
            count = len(siblings)
            
            if self.solitude_mark >= count or count >= self.overpopulation_mark:
                self.dying_cells.append(cell)
                

    def create_newborn_cells(self):
        empty_indices = []
        
        for cell in self.live_cells:
            empty_indices += [
                [sibling[0], sibling[1]] for sibling in cell.get_sibling_indices() 
                if self.within_field(sibling[0], sibling[1])
                    and self.get_cell_at(sibling[0], sibling[1]) == None
            ]

        intersections = {}
            
        for i in empty_indices:
            key = str(i[0]) + '_' + str(i[1])
            intersections[key] = 1 + (intersections[key] if key in intersections else 0)
            
        self.newborn_cells = [
            Cell(*[int(n) for n in key.split("_")]) 
            for key, value in intersections.items() 
            if value == self.newborn_mark
        ]


    def remove_dying_cells(self):
        for cell in self.dying_cells:
            self.remove_cell(cell)
        
        self.dying_cells = []

    def promote_newborn_cells(self):
        for cell in self.newborn_cells:
            self.add_cell(cell)
        
        self.newborn_cells = []
        
    def reset(self):
        self.matrix = [[None for __ in range(self.size)] for _ in range(self.size)]
        self.live_cells = []
        self.dying_cells = []
        self.newborn_cells = []
        
    
        
class Cell():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def get_sibling_indices(self):
        combinations = product([-1, 0, 1], repeat=2)
        return [
            [comb[0] + self.x, comb[1] + self.y] 
            for comb in combinations 
            if (comb[0] != 0 or comb[1] != 0)
        ]
        