from random import choice

moves = {#map moves to what they beat
    'rock' : 'scissors',
    'paper': 'rock',
    'scissors':'paper'
}

def rock_paper_scissors(total_rounds=5):
    comp_wins = 0
    user_wins = 0
    cur_round = 0
    above_half = total_rounds//2 + 1
    while comp_wins < above_half and user_wins < above_half and cur_round < total_rounds:#if player or comp wins more than half the rounds, they win
        comp_move = choice(list(moves.keys()))#get comp move
        user_move = input("Move: ")#get user move
        while user_move not in moves:#make sure the user picked a valid move
            print("Please pick a valid move!")
            user_move = input("Move: ")
        if moves[comp_move] == user_move:#comp beats user
            comp_wins += 1
            print(f"{comp_move} beats {user_move}")
        elif moves[user_move] == comp_move:#user beats comp
            user_wins += 1
            print(f"{user_move} beats {comp_move}")
        else:#tie
            print("tie")
            cur_round -= 1
        cur_round += 1
    return f"Best of {total_rounds} result: Player: {user_wins} vs Comp: {comp_wins}"

print(rock_paper_scissors())