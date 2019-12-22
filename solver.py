import time #used to check script's run time

#class representing a single cell of sudoku board
class Cell:
    def __init__(self, row_number, column_number, value):
        self.row = row_number #0 thru 8
        self.column = column_number #0 thru 8
        self.box = self.set_box_number() #0 thru 8
        self.value = value #0 if empty cell
        self.possibilities = self.set_initial_possibilities() #empty list or 1 thru 9

    #set box number based on row and column number
    def set_box_number(self):
        box_number = int(self.column/3)
        box_number += int(self.row/3)*3
        return box_number

    #set possibilities to empty list if cell not empty or 1 thru 9
    def set_initial_possibilities(self):
        if self.value != 0:
            return []
        else:
            return [*range(1, 10)] 


#class solving sudoku in 'human' way
class Solver:
    def __init__(self, board):
        self.cells = []
        for row_no, row in enumerate(board):
            for col_no, val in enumerate(row):
                self.cells.append(Cell(row_no, col_no, val))
    
    #get all cells from box
    def get_cells_from_box(self, box_number):
        return [cell for cell in self.cells if box_number == cell.box]

    #get all cells from column
    def get_cells_from_column(self, column_number):
        return [cell for cell in self.cells if column_number == cell.column]

    #get all cells from row
    def get_cells_from_row(self, row_number):
        return [cell for cell in self.cells if row_number == cell.row] 

    #get all cells within same box, column and row as given cell
    def get_conflicting_cells(self, given_cell):
        return {cell for cell in self.cells if given_cell.box == cell.box or given_cell.column == cell.column or given_cell.row == cell.row} 

    #remove not valid possibilities from all cells
    def set_all_cells_possibilities(self):
        for cell in self.cells:
            self.remove_cell_value_from_others_possibilities(cell)

    #look for a cell with single possibility and solve it
    def find_and_solve_cell_with_one_possibility(self):
        for cell in self.cells:
            if len(cell.possibilities) == 1:
                self.solve_cell(cell, cell.possibilities[0])
                return True
        return False

    #look for unique possibilities in all boxes, column and rows
    def find_and_solve_unique_possibilities(self):
        for number in range (0, 8):
            if self.if_unique_possibility_within_cells(self.get_cells_from_box(number)):
                return True
            if self.if_unique_possibility_within_cells(self.get_cells_from_column(number)):
                return True
            if self.if_unique_possibility_within_cells(self.get_cells_from_row(number)):
                return True
        return False

    #look for unique possibility in group of cells
    def if_unique_possibility_within_cells(self, same_group_cells):
        counts = [0] * 10
        for cell in same_group_cells:
            for possibility in cell.possibilities:
                counts[possibility] += 1
        if 1 in counts:
            unique_value = counts.index(1)
            for cell in same_group_cells:
                if unique_value in cell.possibilities:
                    self.solve_cell(cell, unique_value)
                    return True
            return False

    #solve cell and remove its value from other cells possibilities
    def solve_cell(self, given_cell, value):
        given_cell.value = value
        given_cell.possibilities = []
        self.remove_cell_value_from_others_possibilities(given_cell)

    #remove cell value from possibilites of cells within same box, column and row
    def remove_cell_value_from_others_possibilities(self, given_cell):
        for conflicting_cell in self.get_conflicting_cells(given_cell):
            try:
                conflicting_cell.possibilities.remove(given_cell.value)
            except:
                continue

    #main algorithm of the class
    def run(self):
        while(True):
            if not self.find_and_solve_cell_with_one_possibility():
                if not self.find_and_solve_unique_possibilities():
                    break


#class solving sudoku with backtracking algorithm
class Backtrack():
    def __init__(self, cells):
        self.cells = cells
        self.unsolved_cells = [cell for cell in self.cells if cell.value == 0]

    #get all cells within same box, column and row as given cell
    def get_conflicting_cells_values(self, given_cell):
        return {cell.value for cell in self.cells if given_cell.box == cell.box or given_cell.column == cell.column or given_cell.row == cell.row} 

    #check validity of sudoku if cell is set to given value
    def if_solution_valid(self, given_cell, cell_value_to_check):
        return not cell_value_to_check in self.get_conflicting_cells_values(given_cell)

    #check current cell value and pick next of its possibilities
    def get_next_possibility(self, given_cell):
        if given_cell.value == 0:
            return given_cell.possibilities[0]
        else:
            return given_cell.possibilities[given_cell.possibilities.index(given_cell.value)+1]

    #main algorithm of the class
    def run(self):
        current_cell_number = 0
        while (current_cell_number >= 0 and current_cell_number < len(self.unsolved_cells)):
            current_cell = self.unsolved_cells[current_cell_number]
            try:
                #get next possibility for cell
                next_possibility = self.get_next_possibility(current_cell)
            except IndexError:
                #no more possibilities for cell -> take step back and work on previous cell
                current_cell.value = 0
                current_cell_number -= 1
            else:
                #possibility valid -> change cell value and proceed to next cell
                if self.if_solution_valid(current_cell, next_possibility):
                    current_cell.value = next_possibility
                    current_cell_number += 1
                #possibility not valid -> change cell value and repeat process
                else:
                    current_cell.value = next_possibility


#class responsible for printing sudoku board in readable form
class Printer():
    def __init__(self, cells):
        self.cells = cells

    #print sudoku board
    def print(self):
        last_cell_row_no = 0
        for cell in self.cells:
            if last_cell_row_no != cell.row:
                print()
            print(cell.value, end = " ")
            last_cell_row_no = cell.row
        print("\n- - - - - - - - -")

#class responsible for checking if sudoku solution is valid
class Validator():
    def __init__(self, cells):
        self.cells = cells

    #check if sudoku solution is valid
    def if_valid(self):
        for cell in self.cells:
            if cell.value == 0:
                return False
        return True

    #print sudoku validity
    def print(self):
        if self.if_valid():
            print("Sudoku solved!")
        else:
            print("Sudoku is not valid!")

### main part below ###
def main():
    
    #sudoku to solve
    sudoku_to_solve = [
    [0, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 8, 0, 0, 0, 7, 0, 9, 0],
    [6, 0, 2, 0, 0, 0, 5, 0, 0],
    [0, 7, 0, 0, 6, 0, 0, 0, 0],
    [0, 0, 0, 9, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 4, 0],
    [0, 0, 5, 0, 0, 0, 6, 0, 3],
    [0, 9, 0, 4, 0, 0, 0, 7, 0],
    [0, 0, 6, 0, 0, 0, 0, 0, 0]
    ]

    start_time = time.time() #start timer to measure run time

    solver = Solver(sudoku_to_solve)

    printer=Printer(solver.cells)
    printer.print()

    solver.set_all_cells_possibilities() #checks possibilities for all cells
    solver.run() #comment this line to leave everything to backtracking

    backtrack=Backtrack(solver.cells)
    backtrack.run()

    printer=Printer(backtrack.cells)
    printer.print()

    validator=Validator(backtrack.cells)
    validator.print()

    print("Run time: %s seconds" % (time.time() - start_time))

if __name__ == "__main__":
    main()