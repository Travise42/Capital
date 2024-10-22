
import time
import random

initial_time = time.time()

def create_board(board_size: int) -> list[list[int]]:
    """ Return an empty board with 'board_size' rows and columns.
    
    Prerequisites:
        board_size >= 4
    """
    
    if board_size < 4:
        raise ValueError
    return [[0 for column in range(board_size)] for row in range(board_size)]
    
def print_board(board: list[list[int]]) -> None:
    """ Print out an array showing the board more clearly.
    """
    
    print(str(board).replace("], ", "]\n")[1:-1])

def spread_city_to(board: list[list[int]], column: int, row: int, city: int) -> bool:
    """ Change an empty space into a city as long as it is on 'board'.
    """
    
    ON_THE_BOARD = 0 <= column < len(board) and 0 <= row < len(board)
    if not ON_THE_BOARD:
        return False
    
    if board[row][column]:
        return False
    
    board[row][column] = city
    return True

def spread_cities(board: list[list[int]]) -> None:
    """ Change an empty space next to every city space wthin 'board' into that city type.
    """
    
    for row in range(len(board)):
        for column in range(len(board)):
            # Ignore empty spaces
            if not board[row][column]:
                continue
            
            dir = random.choice([-1, 1])
            # This prioritizes higher up cities, might need to be changed
            if random.randint(0, 1):
                if spread_city_to(board, column + dir, row, board[row][column]):
                    continue
                if spread_city_to(board, column - dir, row, board[row][column]):
                    continue
            if spread_city_to(board, column, row + dir, board[row][column]):
                continue
            spread_city_to(board, column, row - dir, board[row][column])

def create_capitals(board: list[list[int]]) -> list[tuple[int, int]]:
    """ Creates positions for capitals until a valid orientation is created using recursion.
    """
    
    # Create a valid combination of capitals that wont interfere one another
    #TODO optimize by going backwards
    capitals = []
    
    last_column = -2
    taken_columns = []
    for row in range(len(board)):
        open_columns = [i for i in range(len(board))
                        if i not in taken_columns
                        and (last_column + 1 < i or i < last_column - 1)]
        if len(open_columns) == 0:
            # Not a valid combination of crowns so retry
            return create_capitals(board)
        column = random.choice(open_columns)
        last_column = column
        taken_columns.append(column)
        capitals.append((column, row))
        
    # Add the capitals to the empty board
    for i, (column, row) in enumerate(capitals):
        board[row][column] = i + 1
    
    # Create cities around the capitals
    while not all(square for row in board for square in row):
        spread_cities(board)
                
    return capitals
   
def get_cities(board: list[list[int]]) -> list[list[tuple[int, int]]]:
    """ Returns a list containing a list for each city that contains the
    column and row of each square within the city.
    """
    
    cities = [[] for city in range(len(board))]
    for row in range(len(board)):
        for column in range(len(board)):
            cities[board[row][column] - 1].append((column, row))
        
    return cities

def try_capital(solutions: list[int], board: list[list[int]], cities: list[list[tuple[int, int]]],
                capitals: list[tuple[int, int]], depth: int) -> None:
    """ Increases the first element in 'solutions' by the amount of possible solutions to 'board'.
    
    Prerequisites:
        captials = []
        depth = 0
    """
    
    # End the recurssion after two possibilities are found
    if solutions[0] > 1:
        return
    
    # Found a possible solution! Try to find another
    if depth == len(board):
        solutions[0] += 1
        return
    
    # Guess and check every valid position in this city
    for column, row in cities[depth]:
        for cap_column, cap_row in capitals:
            # Check to see if this capital's position is interfering with another capital's positon
            if column == cap_column or row == cap_row or (-1 <= column - cap_column <= 1 and -1 <= row - cap_row <= 1):
                break
        else:
            # Case: This capital is in a valid position
            try_capital(solutions, board, cities, capitals + [(column, row)], depth + 1)
            
def get_solutions(board: list[list[int]]) -> int:
    """ Returns the amount of possible solutions to 'board'.
    """
    
    # Start recursion loop
    solutions = [0]
    try_capital(solutions, board, sorted(get_cities(board), key=len), [], 0)
    
    return solutions[0]

i = 0
while i < 100 or solutions != 1:
    board = create_board(board_size=12)
    capitals = create_capitals(board)
    solutions = get_solutions(board)
    i += 1

print_board(board)
print("Solutions: " + str(solutions))

print("Time elapsed: " + str(time.time() - initial_time))
