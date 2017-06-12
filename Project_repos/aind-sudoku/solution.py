# from utils import *
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'

# Indivudual squares
boxes = cross(rows, cols)

# Set of 9 boxes that can contain only 123456789
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

# To solve a diagonal sudoku, it is only needed to consider the diagonals as units.

# To generate the diagonals, it is only needed to append the rows and
# columns one by one, not crossing them. The left diagonal uses the
# rows and cols as they are, the right diagonal uses the reversed cols.
diag_l = [[values[0]+values[1] for values in zip(rows, cols)]]
diag_r = [[values[0]+values[1] for values in zip(rows, cols[::-1])]]

unitlist = row_units + col_units + square_units + diag_l + diag_r
units = dict((b, [u for u in unitlist if b in u]) for b in boxes)
peers = dict((s, set(sum(units[s],[])) - set([s])) for s in boxes)

assignments = []

# From Udacity's solution
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Finding the twins
    ## List that will hold all the twins found
    twins = list()
    ## Limit the possible twins to boxes with 2 possible solutions
    possible_twins = [box for box in boxes if len(values[box]) == 2]

    # Search in the peers of the possible twins for repeated values, and append them to the
    # twins list when found
    for box in possible_twins:
        for peer in peers[box]:
            if values[peer] == values[box]:
                twins.append([box, peer])

    # Eliminating values from peers
    ## Search in the peers of both twins for boxes that contain the possible values
    for twin_1, twin_2 in twins:
        value = values[twin_1]
        ## Intersection of two sets allows us to find the peers of both twins
        for peer in peers[twin_1].intersection(peers[twin_2]):
            # Since t1 can be a peer of t2, and viceversa, skip the replacement if a peer
            # with the same value is found
            if value != values[peer]:
                for val in value:
                    assign_value(values, peer, values[peer].replace(val, ''))
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the
            value will be '123456789'.
    """
    numbers = '123456789'
    return {values[0]: numbers if values[1] == '.' else values[1] for values in zip(boxes, grid)}

# From Udacity's solution
def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                        for c in cols))
        if r in 'CF': print(line)
    return

# From Udacity's solution
def eliminate(values):
    """Performs elimination of possible values from peers
        Args:
            values(dict):   Sudoku in dictionary form.
        Returns:
            values(dict):   Sudoku in dictonary form after removing values.
    """
    solved_boxes = [box for box in boxes if len(values[box]) == 1]
    for box in solved_boxes:
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(values[box], ''))
    return values

# From Udacity's solution
def only_choice(values):
    """Checks the units for boxes that only have one possible choice and selects it
            Args:
                values(dict):   Sudoku in dictionary form
            Returns:
                values(dict):   Sudoku in dictionary form after removing the only possible choice.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    '''Applies all the constraints to the puzzle in an attempt
            to solve it. Keeps trying until the constraints no longer yield any changes.
        Args:
            values(dict):   Sudoku in dictionary form
        Returns:
            values(dict):   The dictionary with some solutions.
    '''
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        # Added the naked twins constraint.
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

# From Udacity's solution
def search(values):
    '''Recursively applies DFS to try to solve the puzzle.
        Args:
            values(dict):   Sudoku in dictionary form
        Returns:
            values(dict, bool): If a solution is found return a dictionary with it, else
            it returns False
    '''
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values

    _, box = min([len(values[box]), box] for box in boxes if len(values[box]) > 1)
    for value in values[box]:
        new_sudoku = values.copy()
        new_sudoku[box] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    # diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # diag_sudoku_grid = '.8.4.7.9.3.4...8.2.6.....7.6.......1.........8.......9.1.....3.2.5...1.7.3.8.9.5.'
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
