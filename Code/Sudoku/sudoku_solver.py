def cross(a, b):
    """Returns a list of crossed values"""
    return [s+t for s in a for t in b]

class sudoku_solver():
    """This class solves a 9x9 sudoku."""

    def __init__(self, grid):
        self.rows = 'ABCDEFGHI'
        self.cols = '123456789'
        # Indivudual squares
        self.boxes = cross(self.rows, self.cols)

        # Set of 9 boxes that can contain only 123456789
        self.row_units = [cross(r, self.cols) for r in self.rows]
        self.col_units = [cross(self.rows, c) for c in self.cols]
        self.square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
        self.unit_list = self.row_units + self.col_units + self.square_units

        self.units = dict((b, [u for u in self.unit_list if b in u]) for b in self.boxes)
        # TODO Check why the set of the sum works...
        self.peers = dict((s, set(sum(self.units[s],[])) - set([s])) for s in self.boxes)

        self.values_dict = self.grid_values(grid)

    def grid_values(self, grid):
        """Convert a sudoku grid to a dictionary form.
        Args:
            values_string: A sudoku grid in string form, '.' for empty boxes
        Returns:
            A sudoku in dictonary form. A1:value; value is a number or '123456789' for empty boxes. 
        """
        numbers = '123456789'
        return {values[0]: numbers if values[1] == '.' else values[1] for values in zip(self.boxes, grid)}

    def eliminate(self, values):
        """Performs elimination of possible values from peers
        Args:
            values_dictionary: Sudoku in dictionary form.
        Returns:
            Sudoku in dictonary form after removing values.
        """
        # Solution 2; with the peers dictionary
        solved_boxes = [box for box in self.boxes if len(values[box]) == 1]
        for box in solved_boxes:
            for peer in self.peers[box]:
                values[peer] = values[peer].replace(values[box], '')
        return values

        # Solution 1; without the peers dictionary
        # solved_boxes = [box for box in self.boxes if len(values_dictionary[box]) == 1]
        # for box in solved_boxes:
        #     for unit in self.units[box]:
        #         for unit_value in unit:
        #             if len(values_dictionary[unit_value]) > 1:
        #                 if unit_value != box:
        #                     values_dictionary[unit_value] = values_dictionary[unit_value].replace(values_dictionary[box], "")

        # # # With this code it removes additional possible values if a solution has been found
        # # for box_key, box_value in values_dictionary.items():
        # #     if len(box_value) > 1:
        # #         This goes through all the peers
        # #         for unit in self.unit_list:
        # #             if box_key in unit:
        # #                 for unit_value in unit:
        # #                     if len(values_dictionary[unit_value]) == 1:
        # #                         if unit_value != box_key:
        # #                             values_dictionary[box_key] = values_dictionary[box_key].replace(values_dictionary[unit_value], "")
        return values

    def only_choice(self, values):
        """Checks the units for boxes that only have one possible choice and selects it"""
        for unit in self.unit_list:
            for digit in '123456789':
                dplaces = [box for box in unit if digit in values[box]]
                if len(dplaces) == 1:
                    values[dplaces[0]] = digit
        return values

    def reduce_solution(self, values):
        stalled = False
        while not stalled:
            solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
            values = self.eliminate(values)
            values = self.only_choice(values)
            solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
            stalled = solved_values_before == solved_values_after
            # Sanity check, return False if there is a box with zero available values:
            if len([box for box in values.keys() if len(values[box]) == 0]):
                return False
        return values

    def search(self, values):
        values = self.reduce_solution(values)
        if values is False:
            return False
        if all(len(values[s]) == 1 for s in self.boxes):
            return values 

        # # This adds all the boxes to the search; could potentially be slower
        # unsolved_boxes = {v[0]:v[1] for v in values.items() if len(v[1]) > 1}
        # sorted_uboxes = sorted(unsolved_boxes.items(), key=lambda x: int(x[1]))
        # for box in sorted_uboxes:
        #     for value in values[box[0]]:
        #         new_values = values.copy()
        #         new_values[box[0]] = value
        #         attempt = self.search(new_values)
        #         if attempt:
        #             return attempt
        # # Proposed solution; the heuristic to only consider the minimum box of each grid helps speed it up by reducing the amount of searches.
        n,s = min([len(values[s]),s] for s in self.boxes if len(values[s]) > 1)
        # # Now use recurrence to solve each one of the resulting sudokus, and 
        for value in values[s]:
            new_sudoku = values.copy()
            new_sudoku[s] = value
            attempt = self.search(new_sudoku)
            if attempt:
                return attempt

    def solve(self):
        self.values_dict = self.search(self.values_dict)

    def display(self, values = {}):
        """Displays a grid"""
        values = self.grid_values(values) if len(values) > 1 else self.values_dict
        width = 1+max(len(values[s]) for s in self.boxes)
        line = '+'.join(['-'*(width*3)]*3)
        for r in self.rows:
            print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                            for c in self.cols))
            if r in 'CF': print(line)
        return

if __name__ == '__main__':
    solver = sudoku_solver('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')
    solver.solve()
    solver.display()

    print()

    solver2 = sudoku_solver('4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')
    solver2.solve()
    solver2.display()
