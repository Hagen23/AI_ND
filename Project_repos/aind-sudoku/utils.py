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
diag_l = [[values[0]+values[1] for values in zip(rows, cols)]]
diag_r = [[values[0]+values[1] for values in zip(rows, cols[::-1])]]

unitlist = row_units + col_units + square_units + diag_l + diag_r

units = dict((b, [u for u in unitlist if b in u]) for b in boxes)
peers = dict((s, set(sum(units[s],[])) - set([s])) for s in boxes)


