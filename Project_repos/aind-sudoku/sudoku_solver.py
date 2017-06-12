''' Sudoku Solver 
    Class that takes a Sudoku as a grid as input an can solve it using Constraint propagation and search
    Octavio Navarro
'''

def cross(a, b):
    """Returns a list of crossed values"""
    return [s+t for s in a for t in b]

class sudoku_solver():
    """This class solves a 9x9 sudoku."""

    ## From udacity's solution
    def assign_value(self, values, box, value):
        """
        Please use this function to update your values dictionary!
        Assigns a value to a given box. If it updates the board record it.
        """
        # Don't waste memory appending actions that don't actually change any values
        if values[box] == value:
            return values

        values[box] = value
        if len(value) == 1:
            self.assignments.append(values.copy())
        return values

    def __init__(self, grid, diagonal=False):
        '''Defines and initializes the units, peers, and constrains of the puzzle
            Args:
                grid(string):   A sudoku grid in string form.
                diagonal(bool): To determine if the diagonal constraints are needed.
        '''
        self.rows = 'ABCDEFGHI'
        self.cols = '123456789'
        self.assignments = []

        # Indivudual squares
        self.boxes = cross(self.rows, self.cols)

        # Set of 9 boxes that can contain only 123456789
        self.row_units = [cross(r, self.cols) for r in self.rows]
        self.col_units = [cross(self.rows, c) for c in self.cols]
        self.square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

        # To solve a diagonal sudoku, it is only needed to consider the diagonals as units.
        if diagonal:
            # To generate the diagonals, it is only needed to append the rows and
            # columns one by one, not crossing them. The left diagonal uses the
            # rows and cols as they are, the right diagonal uses the reversed cols.
            diag_l = [[values[0]+values[1] for values in zip(self.rows, self.cols)]]
            diag_r = [[values[0]+values[1] for values in zip(self.rows, self.cols[::-1])]]
            self.unit_list = self.row_units + self.col_units + self.square_units + diag_l + diag_r
        else:
            self.unit_list = self.row_units + self.col_units + self.square_units

        self.units = dict((b, [u for u in self.unit_list if b in u]) for b in self.boxes)
        self.peers = dict((s, set(sum(self.units[s], [])) - set([s])) for s in self.boxes)

        # Stores each sudoku's values as a dictionary
        self.values_dict = self.grid_values(grid)

    def grid_values(self, grid):
        """Convert a sudoku grid to a dictionary form.
        Args:
            values_string(string):  A sudoku grid in string form, '.' for empty boxes
        Returns:
            values(dict):   A sudoku in dictonary form. A1:value; value is
            a number or '123456789' for empty boxes.
        """
        numbers = '123456789'
        return {values[0]: numbers if values[1] == '.' else values[1] for values in zip(self.boxes, grid)}

    def eliminate(self, values):
        """Performs elimination of possible values from peers
        Args:
            values(dict):   Sudoku in dictionary form.
        Returns:
            values(dict):   Sudoku in dictonary form after removing values.
        """
        solved_boxes = [box for box in self.boxes if len(values[box]) == 1]
        for box in solved_boxes:
            for peer in self.peers[box]:
                self.assign_value(values, peer, values[peer].replace(values[box], ''))
                # values[peer] = values[peer].replace(values[box], '')
        return values

    def only_choice(self, values):
        """Checks the units for boxes that only have one possible choice and selects it
            Args:
                values(dict):   Sudoku in dictionary form
            Returns:
                values(dict):   Sudoku in dictionary form after removing the only possible choice.
        """
        for unit in self.unit_list:
            for digit in '123456789':
                dplaces = [box for box in unit if digit in values[box]]
                if len(dplaces) == 1:
                    self.assign_value(values, dplaces[0], digit)
                    # values[dplaces[0]] = digit
        return values

    def naked_twins(self, values):
        """Eliminate values using the naked twins strategy.
        Args:
            values(dict):   Sudoku in dictionary form
        Returns:
            values(dict):   The values dictionary with the naked twins eliminated from peers.
        """
        ## List that will hold all the twins found
        twins = list()
        ## Limit the possible twins to boxes with 2 possible solutions
        possible_twins = [box for box in self.boxes if len(values[box]) == 2]

        ## Search in the peers of the possible twins for repeated values, and append them
        # to the twins list when found
        for box in possible_twins:
            for peer in self.peers[box]:
                if values[peer] == values[box]:
                    twins.append([box, peer])

        ## Search in the peers of both twins for boxes that contain the possible values
        for t1, t2 in twins:
            value = values[t1]
            ## Intersection of two sets allows us to find the peers of both twins
            for peer in self.peers[t1].intersection(self.peers[t2]):
                # Since t1 can be a peer of t2, and viceversa, skip the replacement if
                # a peer with the same value is found
                if value != values[peer]:
                    for v in value:
                        self.assign_value(values, peer, values[peer].replace(v, ''))
                        # values[peer] = values[peer].replace(v, '')
        return values

    def reduce_solution(self, values):
        '''Applies all the strategies, and their constraints, to the puzzle in an attempt
            to solve it. Keeps trying until the strategies no longer yield any changes.
        Args:
            values(dict):   Sudoku in dictionary form
        Returns:
            values(dict):   The dictionary with some solutions.
        '''
        stalled = False
        while not stalled:
            solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
            values = self.eliminate(values)
            values = self.only_choice(values)
            values = self.naked_twins(values)
            solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
            stalled = solved_values_before == solved_values_after
            # Sanity check, return False if there is a box with zero available values:
            if len([box for box in values.keys() if len(values[box]) == 0]):
                return False
        return values

    def search(self, values):
        '''Recursively applies DFS to try to solve the puzzle.
        Args:
            values(dict):   Sudoku in dictionary form
        Returns:
            values(dict, bool): If a solution is found return a dictionary with it, else
            it returns False
        '''
        values = self.reduce_solution(values)
        if values is False:
            return False
        if all(len(values[s]) == 1 for s in self.boxes):
            return values

        # This adds all the boxes to the search, but still uses first the ones with the
        # least amount of possibilities; could potentially be slower
        unsolved_boxes = {v[0]:v[1] for v in values.items() if len(v[1]) > 1}
        sorted_uboxes = sorted(unsolved_boxes.items(), key=lambda x: int(x[1]))
        for box in sorted_uboxes:
            for value in values[box[0]]:
                new_values = values.copy()
                new_values[box[0]] = value
                attempt = self.search(new_values)
                if attempt:
                    return attempt
        # # Proposed udacity's solution; the heuristic to only consider the minimum box
        # of each grid helps speed it up by reducing the amount of searches.
        # n,s = min([len(values[s]),s] for s in self.boxes if len(values[s]) > 1)
        # # # Now use recurrence to solve each one of the resulting sudokus, and
        # for value in values[s]:
        #     new_sudoku = values.copy()
        #     new_sudoku[s] = value
        #     attempt = self.search(new_sudoku)
        #     if attempt:
        #         return attempt

    def solve(self):
        '''Attempts to solve the sudoku.'''
        self.values_dict = self.search(self.values_dict)

    ## From udacity's solution
    def display(self, values={}):
        """Displays a grid.
        Args:
            values(dict):   Sudoku grid to display. If no value is given, displays the
            class' dictionary.
        """
        values = self.grid_values(values) if len(values) > 0 else self.values_dict
        width = 1+max(len(values[s]) for s in self.boxes)
        line = '+'.join(['-'*(width*3)]*3)
        for r in self.rows:
            print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in self.cols))
            if r in 'CF': print(line)

if __name__ == '__main__':
    solver = sudoku_solver('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')
    solver.solve()
    print('\nSimple sudoku\n')
    solver.display()

    print('\n----------------------------\n\nHarder Sudoku\n')

    solver2 = sudoku_solver('4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')
    solver2.solve()
    solver2.display()

    print('\n----------------------------\n\nDiagonal Sudoku\n')

    solver3 = sudoku_solver('2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3', True)
    solver3.solve()
    solver3.display()

    try:
        from visualize import visualize_assignments
        # visualize_assignments(solver.assignments)
        # visualize_assignments(solver2.assignments)
        visualize_assignments(solver3.assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')