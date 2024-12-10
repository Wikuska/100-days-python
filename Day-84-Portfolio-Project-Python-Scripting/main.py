import random

board_squares = {
    1: " ",
    2: " ",
    3: " ",
    4: " ",
    5: " ",
    6: " ",
    7: " ",
    8: " ",
    9: " ",
}

numered_board = """
 1 | 2 | 3 
-----------
 4 | 5 | 6 
-----------
 7 | 8 | 9 
"""

squares_left = [1,2,3,4,5,6,7,8,9]
winning_combinations = [[1,2,3], [4,5,6], [7,8,9], [1,4,7], [2,5,8], [3,6,9], [1,5,9], [3,5,7]]
o_player_squares = []
x_player_squares = []

def turn(player_name, player_shape):
    print(f"{player_name} turn ({player_shape})")
    while True:
        choice = int(input(f"Choose a square ({", ".join([str(x) for x in squares_left])}): "))
        if choice in squares_left:
            squares_left.remove(choice)
            if player_shape == "o":
                o_player_squares.append(choice)
            else:
                x_player_squares.append(choice)
            return choice
        else:
            print("This square is already occupated. Choose another one.")

def board_update(square_num, player_shape):
    board_squares[square_num] = player_shape
    board = f"""
        {board_squares[1]} | {board_squares[2]} | {board_squares[3]} 
       ------------
        {board_squares[4]} | {board_squares[5]} | {board_squares[6]} 
       ------------
        {board_squares[7]} | {board_squares[8]} | {board_squares[9]} 
        """
    return print(board)
    
def check_game_process(o_player_name, x_player_name, player_shape):
    if squares_left == []:
        print("Its a tie!")
        return True
    else:
        if player_shape == "o":
            for combination in winning_combinations:
                if all(square in o_player_squares for square in combination):
                    print(f"{o_player_name} won!")
                    return True
        else:
            for combination in winning_combinations:
                if all(square in x_player_squares for square in combination):
                    print(f"{x_player_name} won!")
                    return True

print("Welcome in tic tac toe game!\n")
print("Enter players names: ")
player_one_name = input("Player one: ")
player_two_name = input("Player two: ")
print("---------------------------------------------------------------")
print("Now we will draw who will start the game!")

o_player = random.choice([player_one_name, player_two_name])
if o_player == player_one_name:
    x_player = player_two_name
else:
    x_player = player_one_name

print(f"{o_player} will start the game!")
print("---------------------------------------------------------------")
print(f"Here is our board numeration, you will need it to place your shapes:\n{numered_board}")
print("Lets start!")
print("---------------------------------------------------------------")

while True:
    o_choice = turn(o_player, "o")
    board_update(o_choice, "o")
    game_end = check_game_process(o_player, x_player, "o")
    if game_end:
        break
    x_choice = turn(x_player, "x")
    board_update(x_choice, "x")
    game_end = check_game_process(o_player, x_player, "x")
    if game_end:
        break
