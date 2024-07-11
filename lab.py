"""
6.101 Lab: Cole Foster
N-Dimenional Mines
Note: docstrings are good and code functions well. May need to fix style.
"""
import doctest


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    keys = ("board", "dimensions", "state", "visible", "mines", "num_hidden")
    for key in keys:
        val = game[key]
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


def new_game_2d(nrows, ncolumns, mines):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
       nrows (int): Number of rows
       ncolumns (int): Number of columns
       mines (list): List of mines, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: ongoing
    visible:
        [False, False, False, False]
        [False, False, False, False]
    mines: {(1, 0), (1, 1), (0, 0)}
    num_hidden: 5
    """
    return new_game_nd((nrows, ncolumns), mines)


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['visible'] to reveal (row, col).  Then, if (row, col) has no
    adjacent mines (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one mine
    is visible on the board after digging (i.e. game['visible'][mine_location]
    == True), 'victory' when all safe squares (squares that do not contain a
    mine) and no mines are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing',
    ...         'mines': {(0,0), (1,0), (1,1)},
    ...         'num_hidden': 4}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: victory
    visible:
        [False, True, True, True]
        [False, False, True, True]
    mines: {(1, 0), (1, 1), (0, 0)}
    num_hidden: 0

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing',
    ...         'mines': {(0,0), (1,0), (1,1)},
    ...         'num_hidden': 4}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    state: defeat
    visible:
        [True, True, False, False]
        [False, False, False, False]
    mines: {(1, 0), (1, 1), (0, 0)}
    num_hidden: 4
    """
    return dig_nd(game, (row, col))


def render_2d_locations(game, all_visible=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (mines), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mines).  game['visible'] indicates which squares should be visible.  If
    all_visible is True (the default is False), game['visible'] is ignored
    and all cells are shown.

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                    by game['visible']

    Returns:
       A 2D array (list of lists)
    """
    return render_nd(game, all_visible)


def render_2d_board(game, all_visible=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       A string-based representation of game
    """
    visible_board = render_2d_locations(game, all_visible)
    output = ""
    for row in visible_board:
        output = output + "".join(row) + "\n"
    return output[:-1]


# N-D IMPLEMENTATION
def make_starting_board(dimensions, symbol=""):
    """
    Creates an empty board with each cell containing a given symbol.

    Parameters:
       dimensions (tuple): Game state
       symbol: The item placed in each cell of the board. Defaults to
       the empty string.

    Returns:
       A len(dimensions) dimensional array (nested lists)
    """
    if len(dimensions) == 1:
        return [symbol] * dimensions[0]
    else:
        return [
            make_starting_board(dimensions[1:], symbol) for _ in range(dimensions[0])
        ]


def get_all_directions(num_dimensions):
    """
    Given a int num_dimensions, returns a list of lists of all possible directions

    Ex: get_all_directions(2) == [[-1,-1], [-1,1], [1,-1], [1,-1],
                                  [1,0], [0, 1], [-1,0], [0,-1]]

    Parameters:
       num_dimensions (int): Number of dimensions. 3 dimensions would contain all
       tuples of size 3 with elements from the set {-1,1,0}, except for (0,0,0).
    Returns:
       List of lists
    """

    def all_directions_including_zero(num_dimensions):
        if num_dimensions == 0:
            return [[]]
        output = []
        for direction in all_directions_including_zero(num_dimensions - 1):
            output.append(direction + [-1])
            output.append(direction + [1])
            output.append(direction + [0])
        return output

    no_zero = all_directions_including_zero(num_dimensions)
    no_zero.remove([0] * num_dimensions)
    return no_zero


def is_valid_index(coordinates, dimensions):
    """
    Given coordinates and the dimensions of the board,
    returns True iff the index is on the board.

    Parameters:
       coordinates (list): Arbitrary coordinates
       dimensions (tuple): Board dimensions

    Returns:
       True if coordinates are on the board, False otherwise
    """
    assert len(coordinates) == len(dimensions)

    for i,_ in enumerate(coordinates):
        if coordinates[i] < 0 or coordinates[i] >= dimensions[i]:
            return False
    return True


def get_all_valid_neighbors(coordinates, dimensions):
    """
    Gets all the neighbors of given coordinate on a board of size dimensions

    Parameters:
       coordinates (list): Specific coordinate
       dimensions (tuple): Board dimensions

    Returns:
       All neighbors of coordinate that are on the board (list of lists)
    """
    assert len(coordinates) == len(dimensions)

    all_neighbors = []
    directions = get_all_directions(len(dimensions))
    for direction in directions:
        output = []
        for idx, value in enumerate(direction):
            output.append(value + coordinates[idx])
        if is_valid_index(output, dimensions):
            all_neighbors.append(output)
    return all_neighbors


def get_value_of_index(coordinates, board):
    """
    Parameters:
       coordinates (tuple): specific coordinates on board
       board (nested lists): Representation of game board

    Returns:
       The value at the given coordinate on this board (various types)
    """
    for dim in coordinates:
        board = board[dim]
    return board


def set_value_of_index(coordinates, board, value):
    """
    Parameters:
       coordinates (tuple): specific coordinates on board
       board (nested lists): Representation of game board
       value (various types): Content of cell on board (bomb, number, etc.)

    """
    if len(coordinates) == 1:
        board[coordinates[0]] = value
    else:
        row = get_value_of_index(coordinates[:-1], board)
        row[coordinates[-1]] = value


def get_all_indices_on_board(dimensions):
    """
    Parameters:
       dimensions (tuple): Dimensions of the board

    Returns:
       List of lists of all coordinates on the board. Used to
       set values on initial board.
    """
    output = []
    if len(dimensions) == 1:
        for i in range(dimensions[0]):
            output.append([i])
        return output
    first = dimensions[0]
    rest = dimensions[1:]
    for index in get_all_indices_on_board(rest):
        for i in range(first):
            output.append([i] + index)
    return output


def get_num_hidden_initial(dimensions):
    """
    Parameters:
       dimensions (tuple): Dimensions of board

    Returns:
       (int) The number of cells that are on the board.
    """
    count = 1
    for i in dimensions:
        count *= i
    return count


def new_game_nd(dimensions, mines):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Args:
       dimensions (tuple): Dimensions of the board
       mines (list): mine locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    """
    board = make_starting_board(dimensions, "")
    for mine in mines:
        set_value_of_index(mine, board, ".")
    for index in get_all_indices_on_board(dimensions):
        if not get_value_of_index(index, board) == ".":
            nearby_mines = 0
            for neighbor in get_all_valid_neighbors(index, dimensions):
                if get_value_of_index(neighbor, board) == ".":
                    nearby_mines += 1
            set_value_of_index(index, board, nearby_mines)

    return {
        "board": board,
        "dimensions": dimensions,
        "state": "ongoing",
        "visible": make_starting_board(dimensions, symbol=False),
        "mines": set(mines),
        "num_hidden": get_num_hidden_initial(dimensions) - len(mines),
    }


def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the visible to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    mine.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one mine is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a mine) and no mines are visible, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    """
    if get_value_of_index(coordinates, game["visible"]):
        return 0  # prevents double counting
    if not game["state"] == "ongoing":
        return 0
    set_value_of_index(coordinates, game["visible"], True)
    if get_value_of_index(coordinates, game["board"]) == ".":
        game["state"] = "defeat"
        return 1
    game["num_hidden"] -= 1
    if game["num_hidden"] == 0:
        game["state"] = "victory"
        return 1
    count = 1
    if get_value_of_index(coordinates, game["board"]) == 0:
        for neighbor in get_all_valid_neighbors(coordinates, game["dimensions"]):
            count += dig_nd(game, neighbor)
    return count


def render_nd(game, all_visible=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (mines), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mines).  The game['visible'] array indicates which squares should be
    visible.  If all_visible is True (the default is False), the game['visible']
    array is ignored and all cells are shown.

    Args:
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       An n-dimensional array of strings (nested lists)

    """
    output = make_starting_board(game["dimensions"])
    if all_visible:
        for coordinate in get_all_indices_on_board(game["dimensions"]):
            to_set = str(get_value_of_index(coordinate, game["board"]))
            if to_set == "0":
                to_set = " "
            set_value_of_index(coordinate, output, to_set)
    if not all_visible:
        for coordinate in get_all_indices_on_board(game["dimensions"]):
            if not get_value_of_index(coordinate, game["visible"]):
                set_value_of_index(coordinate, output, "_")
            else:
                to_set = str(get_value_of_index(coordinate, game["board"]))
                if to_set == "0":
                    to_set = " "
                set_value_of_index(coordinate, output, to_set)
    return output


if __name__ == "__main__":
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests
    pass
