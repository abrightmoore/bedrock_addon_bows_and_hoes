#  @TheWorldFoundry
import math
import json

def write_json(filename, json_object):
    with open(filename, "w") as outfile:
        json.dump(json_object, outfile, indent=4, sort_keys=True)


SAMPLE = {
          "format_version": "1.12",
          "minecraft:recipe_shaped": {
            "description": {
            "identifier": "minecraft:bread"
            },

            
            "tags": [ "crafting_table" ],
            "pattern": [
              "###"
            ],
            "key": {
              "#": {
                "item": "minecraft:wheat"
              }
            },
            "result": {
              "item": "minecraft:bread"
            }
          }
        }

def increment_by_1(board, pos, modulo):
    if pos < len(board):
        carry = 0
        digit = board[pos]
        digit += 1
        if digit >= modulo:
            digit = 0
            carry = 1
        board[pos] = digit
        if carry > 0:
            board = increment_by_1(board, pos+1, modulo)
        return board
    return None  # No new board possible, we are at the maximum


def print_board(board):
    sz = int(math.sqrt(len(board)))
    div = ""
    for i in xrange(0, sz):
        div = div + "-"
        if i < sz-1:
            div = div + "+"

    pieces = " XO"
    for y in xrange(0, sz):
        row = ""
        for x in xrange(0, sz):
            row = row+pieces[board[y*sz+x]]
            if len(row) < sz*2-1:
                row = row + "|"
        print row
        if y < sz-1:
            print div

def evaluate_legal(board, piece1, piece2):  # Either side may go first
    piece_count = 0
    for i in board:
        if i == piece1:
            piece_count += 1
        if i == piece2:
            piece_count -= 1
    # print board, piece_count
    return piece_count


def evaluate_win(board, piece):
    # Check if a particular side has won
    sz = int(math.sqrt(len(board)))

    # Vertical
    for col in xrange(0, sz):
        count_pieces = 0
        for row in xrange(0, sz):
            if board[row*sz+col] == piece:
                count_pieces += 1
        if count_pieces == sz:
            # print "Vertical",str(col)
            return True
    
    # Horizontal
    for row in xrange(0, sz):
        count_pieces = 0
        for col in xrange(0, sz):
            if board[row*sz+col] == piece:
                count_pieces += 1
        if count_pieces == sz:
            # print "Horizontal",str(row)
            return True

    # Diagonal TLBR
    count_pieces = 0
    for pos in xrange(0, sz):
        if board[pos*sz+pos] == piece:
                count_pieces += 1
    if count_pieces == sz:
        # print "Diagonal TLBR"
        return True

    # Diagonal TRBL
    count_pieces = 0
    for pos in xrange(0, sz):
        if board[pos*sz+(sz-1-pos)] == piece:
                count_pieces += 1
    if count_pieces == sz:
        # print "Diagonal TRBL"
        return True
    
    return False

def clone_board(board):
    new_board = []
    for i in board:
        new_board.append(i)
    return new_board


results_win_x = []
results_win_o = []
results_legal_no_win = []

board = [0,0,0,0,0,0,0,0,0]
modulo = 3  # Space is 0, X is 1, O is 2
keep_going = True
while keep_going == True:
    # Try to increment the board by 1
    pos = 0
    new_board = increment_by_1(board, pos, modulo)
    if new_board is not None:  # Check the characteristics of the new board. Is it legal? Does either side win?
        board = new_board
        piece_delta = evaluate_legal(board, 1, 2)
        is_legal = False
        if abs(piece_delta) < 2:
            is_legal = True
        if is_legal:
            is_win_x = evaluate_win(board, 1)
            is_win_o = evaluate_win(board, 2)
            if is_win_x and is_win_o:
                is_legal = False  # Both cannot win. There can be only one
        if is_legal:
            if is_win_x:
                # print("A win for X:")
                
                results_win_x.append(clone_board(board))
                # print board
            if is_win_o:
                # print("O wins!")
                results_win_o.append(clone_board(board))
            if is_win_x == False and is_win_o == False:
                # print_board(board)
                results_legal_no_win.append(clone_board(board))
            # print("")
    else:
        keep_going = False

#  Now we know all the board configurations for winning and legal moves
print("X wins " + str(len(results_win_x)) + " times")
print("O wins " + str(len(results_win_o)) + " times")
print("Other legal board configurations " + str(len(results_legal_no_win)))

# Create shaped recipes for each win configuration

def make_string_from_board(board, pieces):
    result = ""
    for i in board:
        result = result + pieces[i]
    # print result
    return result

def make_recipe_from_board(board, reward):
    # Assumes 3x3 layout
    # print board
    id = make_string_from_board(board, " XO")
    
    pattern = []
    pattern.append(id[0:3:1])
    pattern.append(id[3:6:1])
    pattern.append(id[6:9:1])
    
    recipe = {
          "format_version": "1.12",
          "minecraft:recipe_shaped": {
            "description": {
            "identifier": id.replace(" ", "_").lower()
            },

            "tags": [ "crafting_table" ],
            "pattern": pattern,
            "key": {
              "X": {
                "item": "minecraft:bow"
              },
              "O": {
                "item": "minecraft:wooden_hoe"
              }
            },
            "result": {
              "item": reward
            }
          }
        }
    return recipe

counter = 0

for board in results_win_x:
    counter += 1
    recipe = make_recipe_from_board(board, "minecraft:diamond")
    write_json(make_string_from_board(board, "_xo")+".json", recipe)
    
for board in results_win_o:
    counter += 1
    recipe = make_recipe_from_board(board, "minecraft:emerald")
    write_json(make_string_from_board(board, "_xo")+".json", recipe)
    
    