import copy

# Defining constants for the board
X = "X"  # Represents player X
O = "O"  # Represents player O
EMPTY = None  # Represents an empty cell on the board

# Function to initialize the board configuration
def initial_board():
    return [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]
    ]

# Function to display the current state of the board
def display_board(board):
    for row in board:
        print(row)
    print()

# Player function: Returns the current player
def player(board):
    # Count number of X's and O's on the board
    X_count = sum(row.count(X) for row in board)
    O_count = sum(row.count(O) for row in board)
    
    # X always starts first, so if counts are equal, it's X's turn
    if X_count == O_count:
        return X
    else:
        return O

# Actions function: Returns available actions (empty spots)
def actions(board):
    possible_actions = set()

    # Iterate over each row and cell to find empty space
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))  # Add the empty spot to possible actions
    return possible_actions

# Result function: Returns new board state after a player makes a move
def result(board, action):
    # Raise an error if the move is invalid
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError("Invalid move!")
    
    # Create a new board to avoid modifying the original
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)  # Update the new board with the player's move
    return new_board

# Winner function: Checks if either player has won the game
def winner(board):
    # Check rows and columns for a win
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]  # Return the winner (X or O)
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]  # Return the winner (X or O)
    
    # Check diagonals for a win
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]  # Return the winner (X or O)
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]  # Return the winner (X or O)
    
    return None  # Return None if there is no winner

# Terminal function: Checks if the game is over
def terminal(board):
    # The game is over if there is a winner or no empty spots left
    return winner(board) is not None or all(cell != EMPTY for row in board for cell in row)

# Utility function: Returns the utility of the board
def utility(board):
    # 1 if X has won, -1 if O has won, 0 if it's a tie
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

# Minimax algorithm for AI
def minimax(board):
    if terminal(board):
        return None  # Return None if the game is over

    current_player = player(board)

    # If it's X's turn, maximize the score
    if current_player == X:
        best_value = -float("inf")
        best_move = None
        
        # Evaluate all possible actions for X
        for action in actions(board):
            value = min_value(result(board, action))  # Get the value for the resulting board

            # If this value is better than the best_value found so far, update best_value and best_move
            if value > best_value:
                best_value = value
                best_move = action
        
        return best_move  # Return the best move for X
    else:  # If it's O's turn, minimize the score
        best_value = float("inf")
        best_move = None

        # Evaluate all possible actions for O
        for action in actions(board):
            value = max_value(result(board, action))  # Get the value for the resulting board

            # If this value is better than the best_value found so far, update best_value and best_move
            if value < best_value:
                best_value = value
                best_move = action
        
        return best_move  # Return the best move for O

# Helper function for minimax to get the maximum value
def max_value(board):
    if terminal(board):
        return utility(board)  # Return utility if game is over
    
    value = -float("inf")
    for action in actions(board):
        value = max(value, min_value(result(board, action)))  # Get the maximum value from the minimax search
    return value

# Helper function for minimax to get the minimum value
def min_value(board):
    if terminal(board):
        return utility(board)  # Return utility if game is over
    
    value = float("inf")
    for action in actions(board):
        value = min(value, max_value(result(board, action)))  # Get the minimum value from the minimax search
    return value

# Function to let the human player make a move
def human_move(board):
    while True:
        move = input("Enter your move (row, column): ")  # Prompt the player for their move
        row, col = map(int, move.split(","))  # Split the input into row and column
        if (row, col) in actions(board):  # Check if the move is valid
            return (row, col)  # Return the valid move
        else:
            print("Invalid move, try again.")  # Prompt again if the move is invalid

# Main game loop function
def play_game():
    board = initial_board()  # Initialize the game board
    display_board(board)  # Display the initial board

    while not terminal(board):  # Loop until the game is over
        current_player = player(board)  # Determine the current player
        if current_player == X:  # If it's X's turn (human)
            print("Your turn!")
            action = human_move(board)  # Get the human move
        else:  # If it's O's turn (AI)
            print("AI is making its move...")
            action = minimax(board)  # Get the AI move using minimax

        board = result(board, action)  # Update the board with the chosen action
        display_board(board)  # Display the updated board

    # Determine the winner and print the result
    if winner(board) == X:
        print("You win!")  # If X wins
    elif winner(board) == O:
        print("AI wins!")  # If O wins
    else:
        print("It's a tie!")  # If it's a tie

# Run the game
play_game()
