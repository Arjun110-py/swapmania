import time

# EMPTY = 0
# NORMAL = 1
# SLIDE = 2
# IMMOVABLE = 3
# SWAP = 4
# ROTATE_C = 5
# ROTATE_CC = 6
# CYCLE_C = 7
# CYCLE_CC = 8
# DUPLICATE = 9
OFFSETS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
CYCLES = [(1, 2), (3, 1), (0, 3), (1, 0)]
CYCLES_CC = [(3, 2), (1, 2), (1, 0), (3, 0)]

class Cell:
    def __init__(self, celltype, rotation):
        self.celltype = celltype
        self.rotation = rotation
        self.x = 0
        self.y = 0

    def copy(self):
        return Cell(self.celltype, self.rotation)

    def movable(self, direction):
        match self.celltype:
            case 2: return direction % 2 == self.rotation % 2
            case 3: return False
            case _: return True

    def run(self, board):
        (offset_x, offset_y) = OFFSETS[self.rotation]
        beside_x, beside_y = self.x + offset_x, self.y + offset_y
        beside = board[beside_y][beside_x]
        
        surroundings = [board[self.y + OFFSETS[i][1]][self.x + OFFSETS[i][0]] for i in range(4)]
        surroundings_x = [self.x + OFFSETS[i][0] for i in range(4)]
        surroundings_y = [self.y + OFFSETS[i][1] for i in range(4)]
        
        match self.celltype:
            case 4:
                if beside.movable(self.rotation):
                    print("MOVE")
                    board[self.y][self.x] = beside
                    
                    beside.x, self.x = self.x, beside.x
                    beside.y, self.y = self.y, beside.y
                    
                    board[beside_y][beside_x] = self
            case 5:
                for cell in surroundings: cell.rotation = (cell.rotation + 1) % 4
            case 6:
                for cell in surroundings: cell.rotation = (cell.rotation - 1) % 4
            case 7:
                if all([cell.movable(CYCLES[i][0]) and cell.movable(CYCLES[i][1]) for i, cell in enumerate(surroundings)]):
                    for i, cell in enumerate(surroundings):
                        cell.rotation = (cell.rotation + 1) % 4
                        board[surroundings_y[(i + 1) % 4]][surroundings_x[(i + 1) % 4]] = cell
                        cell.x, cell.y = surroundings_x[(i + 1) % 4], surroundings_y[(i + 1) % 4]
            case 8:
                if all([cell.movable(CYCLES_CC[i][0]) and cell.movable(CYCLES_CC[i][1]) for i, cell in enumerate(surroundings)]):
                    for i, cell in enumerate(surroundings):
                        cell.rotation = (cell.rotation - 1) % 4
                        board[surroundings_y[(i - 1) % 4]][surroundings_x[(i - 1) % 4]] = cell
                        cell.x, cell.y = surroundings_x[(i - 1) % 4], surroundings_y[(i - 1) % 4]
            case 9:
                board[beside_y][beside_x] = surroundings[(self.rotation + 2) % 4].copy()
                board[beside_y][beside_x].x, board[beside_y][beside_x].y = beside_x, beside_y


    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.celltype}:{self.rotation}"

class Board:
    def __init__(self, cells, rotations):
        self.cells = [[Cell(3, 0) for _ in cells[0] + [0, 0]]]
        for cell_row, rot_row in zip(cells, rotations):
            row = [Cell(3, 0)]
            for cell, rotation in zip(cell_row, rot_row):
                row.append(Cell(cell, rotation))
            row.append(Cell(3, 0))
            self.cells.append(row)
        self.cells.append([Cell(3, 0) for _ in cells[0] + [0, 0]])

        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                cell.x, cell.y = x, y

    def run(self):
        subsets = [[] for _ in range(4)]
        for row in self.cells:
            for cell in row:
                match cell.celltype:
                    case 0 | 1 | 2 | 3:
                        continue
                    case 4:
                        subsets[3].append(cell)
                    case 5 | 6:
                        subsets[0].append(cell)
                    case 7 | 8:
                        subsets[2].append(cell)
                    case 9:
                        subsets[1].append(cell)

        for subset in subsets:
            for cell in subset:
                cell.run(self.cells)

    def __repr__(self):
        return str(self)
        
    def __str__(self):
        string = ""
        for row in self.cells:
            for cell in row:
                string += str(cell) + " "
            string += "\n"
        return string

board = Board([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
    [0, 0, 0, 0, 7, 0, 9, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
], [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

while True:
    print(board)
    board.run()
    time.sleep(0.2)