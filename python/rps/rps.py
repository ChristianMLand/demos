from random import choice

moves = {#map potential moves to what they beat
    'rock' : 'scissors',
    'paper' : 'rock',
    'scissors' : 'paper'
}

def rock_paper_scissors(total_rounds=5):
    comp_wins,user_wins,cur_round = 0,0,0
    above_half = total_rounds//2 + 1
    while comp_wins < above_half and user_wins < above_half and cur_round < total_rounds:#if player or comp wins more than half the rounds, they win
        comp_move = choice(list(moves.keys()))#get comp move
        while (user_move := input("Move: ")) not in moves:#make sure the user picked a valid move
            print("Please pick a valid move!")
        if moves[comp_move] == user_move:#comp beats player
            comp_wins += 1
            print(f"Comp: {comp_move} beats Player: {user_move}")
        elif moves[user_move] == comp_move:#player beats comp
            user_wins += 1
            print(f"Player: {user_move} beats Comp: {comp_move}")
        else:#tie
            print("tie")
        cur_round += 1
    return f"Best of {total_rounds} result: Player: {user_wins} vs Comp: {comp_wins} ({total_rounds-user_wins-comp_wins} ties)"

print(rock_paper_scissors())