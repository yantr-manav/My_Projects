
def print_board(xState, oState):
    zero = 'X' if xState[0] else ('O' if oState[0] else 0)
    one = 'X' if xState[1] else ('O' if oState[1] else 1)
    two = 'X' if xState[2] else ('O' if oState[2] else 2)
    three = 'X' if xState[3] else ('O' if oState[3] else 3)
    four = 'X' if xState[4] else ('O' if oState[4] else 4)
    five = 'X' if xState[5] else ('O' if oState[5] else 5)
    six = 'X' if xState[6] else ('O' if oState[6] else 6)
    seven = 'X' if xState[7] else ('O' if oState[7] else 7)
    eight = 'X' if xState[8] else ('O' if oState[8] else 8)
    
    print(f"{zero} | {one} | {two}")
    print(f"--|---|---")
    print(f"{three} | {four} | {five}")
    print(f"--|---|---")
    print(f"{six} | {seven} | {eight}")
    

def check_winner(xState,oState):
    winning_combinations = [
        [0,1,2],[3,4,5],[6,7,8], # horizontal rows
        [0,4,8],[2,4,6],[0,3,6], # vertical columns
        [1,4,7],[2,5,8] # diagonal lines
    ]
    for combo in winning_combinations:
        if (sum(xState[i] for i in combo) == 3):
            print("X wins!")
            return "X wins!"
        elif (sum(oState[i] for i in combo) == 3):
            print("O wins!")
            return "O wins!"
    return None


if __name__ == "__main__":
    xState = [0] * 9
    oState = [0] * 9
    turn = 1    # Player  X starts and 0 for Player O
    print("This is the Tic Tac Toe game module. Let's play!")
    
    while True:

        if turn == 1:
            print("\nX's Chance:")
            value = int(input("Enter the position(0-8):"))
            xState[value] = 1
       
        else:
            print("\nO's Chance:")
            value = int(input("Enter the position(0-8):"))
            oState[value] = 1
        
        print_board(xState,oState)
        check_state = check_winner(xState,oState)
        if(check_state!= None):
            print("Match Over!")
            break        
        turn = 1- turn # for switching turns
        
        
        