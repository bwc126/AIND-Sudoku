assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [['A1','B2','C3','D4','E5','F6','G7','H8','I9'],['A9','B8','C7','D6','E5','F4','G3','H2','I1']]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

unitlist_2 = row_units + column_units + square_units
units_2 = dict((s, [u for u in unitlist_2 if s in u]) for s in boxes)
peers_2 = dict((s, set(sum(units_2[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
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

    # Find all instances of naked twins
    # For each box with more than one value
    unsolved_values = [box for box in values.keys() if len(values[box]) == 2]
    for box in unsolved_values:
        val_1 = values[box]
        for peer in peers[box]:
            val_2 = values[peer]
            # If there's another box in this unit with the same value
            if val_1 == val_2:
                # unsolved_values.remove(box)
                # unsolved_values.remove(peer)
                print (val_1, val_2)
                removal_list = [peer2 for peer2 in peers[box] if peer2 != peer and len(values[peer2]) > 1]
                removal_list_2 = [peer2 for peer2 in peers[peer] if peer2 != box and len(values[peer2]) > 1]

                # removal_list.extend(removal_list_2)
                for box2 in removal_list:
                    # We have our twins, and we can remove their values from other boxes in the same unit.
                    if box2 in removal_list_2:
                        for val in val_1:
                            print(val, box2)
                            values = assign_value(values, box2, values[box2].replace(val, ''))
    return values
    # Eliminate the naked twins as possibilities for their peers


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    # Where we'll put the possible and known grid values for now
    chars = []
    digits = '123456789'
    # We need to convert each full stop into a naive list of possible outcomes, our digits 1 through 9
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    # We should have a total of 81 values in our list for a 9x9 puzzle grid
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    if values:
        # Our width for each box should only be as small as our longest value
        width = 1+max(len(values[s]) for s in boxes)
        # Using the width found above, we build divider strings to separate square units
        line = '+'.join(['-'*(width*3)]*3)
        for r in rows:
            print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                          for c in cols))
            if r in 'CF': print(line)
        print

def eliminate(values):
    # Get each known single value in the puzzle
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    # For each of these solved values, we make sure that any indeterminate peers lose the value of this solved box as a possibility.
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    # Return the puzzle with the solved values removed from the indeterminate boxes of their peers.
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]),s) for s in boxes if len(values[s]) > 1)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
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
    values = grid_values(grid)
    values = search(values)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
