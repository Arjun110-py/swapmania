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
# TRASH = 10
OFFSETS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
CYCLES = [(1, 2), (3, 1), (0, 3), (1, 0)]
CYCLES_CC = [(3, 2), (1, 2), (1, 0), (3, 0)]
TRANSPARENT = [10]

def str_matrix(board):
    string = ""
    for row in board:
        for cell in row:
            string += str(cell) + " "
        string += "\n"
    return string

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
            case 10: return True
            case _: return True

    def effect(self, cell, board):
        match self.celltype:
            case 10:
                board[cell.y][cell.x] = Cell(0, 0)
                board[cell.y][cell.x].x, board[cell.y][cell.x].y = cell.x, cell.y

    def replaceable(self, direction):
        match self.celltype:
            case 2: return direction % 2 == self.rotation % 2
            case 3: return False
            case 10: return False
            case _: return True

    def run(self, board):
        (offset_x, offset_y) = OFFSETS[self.rotation]
        beside_x, beside_y = self.x + offset_x, self.y + offset_y
        beside = board[beside_y][beside_x]

        surroundings = [board[self.y + OFFSETS[i][1]][self.x + OFFSETS[i][0]] for i in range(4)]
        surroundings_pos = [(cell.x, cell.y) for cell in surroundings]

        match self.celltype:
            case 4:
                if beside.movable(self.rotation):
                    if beside.celltype not in TRANSPARENT:
                        board[self.y][self.x] = beside

                        beside.x, self.x = self.x, beside_x
                        beside.y, self.y = self.y, beside_y

                        board[beside_y][beside_x] = self
                    else: beside.effect(self, board)
            case 5:
                for cell in surroundings: cell.rotation = (cell.rotation + 1) % 4
            case 6:
                for cell in surroundings: cell.rotation = (cell.rotation - 1) % 4
            case 7:
                if all([cell.movable(CYCLES[i][0]) and \
                        cell.movable(CYCLES[i][1]) for i, cell in enumerate(surroundings)]):
                    prev_move = surroundings[-1].celltype not in TRANSPARENT
                    transparents = []
                    
                    for i, cell in enumerate(surroundings):
                        if prev_move: cell.effect(surroundings[i - 1], board)
                        prev_move = cell.celltype not in TRANSPARENT
                        transparents.append(not prev_move)
                        
                    for i, cell in enumerate(surroundings):
                        if not transparents[i] and not transparents[(i + 1) % 4]:
                            cell.rotation = (cell.rotation + 1) % 4
                            board[surroundings_pos[(i + 1) % 4][1]][surroundings_pos[(i + 1) % 4][0]] = cell
                            
                            if transparents[i - 1]:
                                board[cell.y][cell.x] = Cell(0, 0)
                                board[cell.y][cell.x].x, board[cell.y][cell.x].y = cell.x, cell.y
                                
                            (cell.x, cell.y) = surroundings_pos[(i + 1) % 4]
            case 8:
                if all([cell.movable(CYCLES_CC[i][0]) and \
                        cell.movable(CYCLES_CC[i][1]) for i, cell in enumerate(surroundings)]):
                            prev_move = surroundings[0].celltype not in TRANSPARENT
                            transparents = []

                            for i, cell in reversed(list(enumerate(surroundings))):
                                if prev_move: cell.effect(surroundings[(i + 1) % 4], board)
                                prev_move = cell.celltype not in TRANSPARENT
                                transparents.append(not prev_move)

                            transparents = list(reversed(transparents))
                            
                            for i, cell in enumerate(surroundings):
                                if not transparents[i] and not transparents[i - 1]:
                                    cell.rotation = (cell.rotation - 1) % 4
                                    board[surroundings_pos[i - 1][1]][surroundings_pos[i - 1][0]] = cell

                                    if transparents[(i + 1) % 4]:
                                        board[cell.y][cell.x] = Cell(0, 0)
                                        board[cell.y][cell.x].x, board[cell.y][cell.x].y = cell.x, cell.y

                                    (cell.x, cell.y) = surroundings_pos[i - 1]
            case 9:
                if board[beside_y][beside_x].replaceable(self.rotation):
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
        return str_matrix(self.cells)

board = Board([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 5],
    [4, 0, 0, 2, 0, 0, 0, 7, 0, 0, 10],
    [0, 0, 0, 0, 0, 9, 0, 0, 8, 0, 0],
    [0, 0, 0, 6, 6, 0, 0, 0, 0, 0, 0]
], [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

print(board)
input("Press Enter to Run")
while True:
    board.run()
    print(board)
    input("Press Enter to continue")