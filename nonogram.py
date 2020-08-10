#Program which solves a nonogram matrix

import math

#magic variables


Black = 1
White = 0
Empty = -1


#helpfull function


def check_if_legal(row, blocks):
    """checks if a complete row is correct according the blocks"""
    counter = 0
    compare_lst = []
    for square in row:
        if square == Black:
            counter += 1
        else:
            if counter > 0:
                compare_lst.append(counter)
                counter = 0
    if counter > 0:
        compare_lst.append(counter)
    if compare_lst == blocks:
        return True
    return False




# part b function number 1

def get_row_variations(row, blocks):
    """:returns a list of lists with all the options to solve a given row"""
    if check_if_possible(row, blocks):
        first_attempt = easy_cases(row, blocks)
        if first_attempt != []:
            return first_attempt
        if row == len(row) * [Empty]:
            answers_lst = []
            option_lst = row_options(row, blocks)
            for optional_row in option_lst:
                temp_lst = get_row_variations(optional_row, blocks)
                for var_row in temp_lst:
                    if check_if_legal(var_row, blocks):
                        answers_lst.append(var_row)
            return answers_lst
        all_options = backtracking_row_variation(row, len(row) - 1, blocks)
        final_list = []
        for option in all_options:
            if check_if_legal(option, blocks):
                final_list.append(option)
        return final_list
    return []

#the main function that helps get_row_variation find all the rows options

def backtracking_row_variation(row, n, blocks):
    """:returns all the row optional solves using backtracking method"""
    copy_row = row[:]
    final_lst = []
    if n > -1:
        if len(blocks) == 1:
            if copy_row.count(Black) == blocks[0]:
                copy_row = [White if x == Empty else x for x in copy_row]
                final_lst.append(copy_row)
                return final_lst
        if row[n] == Empty:
            copy_row[n] = White
            option_lst = backtracking_row_variation(copy_row, n - 1, blocks)
            for option in option_lst:
                final_lst.append(option)
            copy_row[n] = Black
            option_lst = backtracking_row_variation(copy_row, n-1, blocks)
            for optional_row in option_lst:
                final_lst.append(optional_row)
        else:
            option_lst = (backtracking_row_variation(copy_row, n - 1, blocks))
            for var_row in option_lst:
                final_lst.append(var_row)
        return final_lst
    final_lst.append(copy_row)
    return final_lst

#some functions that deals with certain situations, with their help the searching time is faster


def check_if_possible(row, blocks):
    """:returns True if the row is mathematically possible to be solved"""
    if len(row) < (len(blocks) - 1) + sum(blocks):
        return False
    return True


def easy_cases(row, blocks):
    """:returns a solved row for few easy cases"""
    if blocks == []:
        return [[0 for j in range(len(row))]]
    if len(blocks) == 1 and sum(blocks) == len(row):
            return [[Black for i in range(len(row))]]
    if len(blocks) - 1 + sum(blocks) == len(row):
        new_row = []
        for i in blocks:
            new_row.extend([Black for k in range(i)])
            new_row.append(White)
        new_row.pop()
        return new_row
    return []



def row_options(row, blocks):
    """:returns all the row options according to his last block"""
    if len(blocks) == 1:
        return find_row_option(row, blocks)
    else:
        new_row = [-1 for i in range(len(row) - (blocks[0] + 1))]
        remember_block = blocks[0]
        blocks.pop(0)
        list_of_answers = row_options(new_row, blocks)
        blocks.insert(0, remember_block)
        final_lst = []
        for j in list_of_answers:
            final_lst.append([-1 for k in range(remember_block + 1)]+ j)
        return final_lst


def find_row_option(row, block):
    """:argument an empty row and a single block
    :returns all the options"""
    answers = []
    for j in range(len(row) - block[0] + 1):
        option = [Empty for i in range(len(row))]
        for k in range(block[0]):
            option[j] = 1
            j += 1
        count = -1
        while option[count] != 1:
            option[count] = 0
            count -= 1
        answers.append(option)
    return answers






#part b function 2



def get_intersection_row(rows):
    """returns the rows mutual objects as a row"""
    final_row = []
    if len(rows) == 1:
        return rows[0]
    for j in range(len(rows[0])):
        counter = 0
        for i in range(len(rows) - 1):
            if rows[i][j] == rows[i + 1][j]:
                counter += 1
        if counter == len(rows) - 1:
            final_row.append(rows[0][j])
        else: final_row.append(Empty)
    return final_row


#part c function 3 solution


def solve_easy_nonogram(constraints):
    """returns a solved board of easy"""
    game_board = board(constraints)
    solution = solve_if_easy(game_board, constraints)
    return solution





def solve_if_easy(board, constraints):
    """:returns a solved board as much as possible"""
    temp_board = board[:]
    for i in range(len(temp_board)):
        var_lst = get_row_variations(temp_board[i], constraints[0][i])
        if var_lst == []:
            return None
        temp_board[i] = get_intersection_row(var_lst)

    temp_board = board_for_columns(temp_board)

    for k in range(len(temp_board)):
        var_lst = get_row_variations(temp_board[k], constraints[1][k])
        if var_lst == []:
            return None
        temp_board[k] = get_intersection_row(var_lst)

    temp_board = board_back_to_rows(temp_board)

    if temp_board == board:
        return temp_board
    else:
        return solve_if_easy(temp_board, constraints)



#board related functions



def board(constraints):
    """build a board according to the constraints given"""
    rows = len(constraints[0])
    columns = len(constraints[1])
    board = []
    for i in range(rows):
        board.append([Empty for k in range(columns)])
    return board


def board_for_columns(board):
    """:argument an ordinary board
    :returns board orgenized from up to down"""
    temp_mat = []
    for i in range(len(board[0])):
        row = []
        for j in board:
            row.append(j[i])
        temp_mat.append(row)
    return temp_mat


def board_back_to_rows(board_for_columns):
    """:argument a boards from up to down
    :returns an ordinary board"""
    new_board = []
    for j in range(len(board_for_columns[0])):
        temp_board = []
        for k in board_for_columns:
            temp_board.append(k[j])
        new_board.append(temp_board)
    return new_board




#part 4 full solution

def solve_nonogram(constraints):
    """:return all the possible solution of the nonogram"""
    game_board = solve_easy_nonogram(constraints)
    if game_board == None:
        return game_board
    else:
        return solve_even_if_not_easy(game_board, constraints)


def solve_even_if_not_easy(board, constraints):
    """:returns all the options for solved board with no empty squares"""
    new_board = board[:]
    temp_board = solve_if_easy(new_board, constraints)
    answers = []
    if temp_board == None:
        return None
    if no_negative_one(temp_board):
        answers.append(temp_board)
        return answers

    neg_one_ind = find_negative_one(temp_board)

    temp_board[neg_one_ind[0][0]][neg_one_ind[1][0]] = White
    answers.append(solve_even_if_not_easy(temp_board, constraints))
    temp_board[neg_one_ind[0][0]][neg_one_ind[1][0]] = Black
    answers.append(solve_even_if_not_easy(temp_board, constraints))

    return answers


#functions regarding empty squares

def no_negative_one(board):
    """:returns True if there are no empty squares in the board and False if there are"""
    count = 0
    for row in board:
        if -1 in row:
            count += 1
    if count > 0:
        return False
    return True


def find_negative_one(board):
    """:returns the index of an empty square in the board"""
    temp_lst = []
    final_lst = []
    for row in board:
        for square in row:
            if square == Empty:
                temp_lst.append(board.index(row))
                final_lst.append(temp_lst)
                temp_lst = []
                temp_lst.append(row.index(square))
                final_lst.append(temp_lst)
                return final_lst



#part d function 5


def count_row_variations(length, blocks):
    """:returns an int object which represent the number of option the row can be solved"""
    sum_blocks = sum(blocks)
    len_blocks = len(blocks)
    n = len_blocks + 1
    k = length - sum_blocks - (len_blocks - 1)
    if k < 0:
        return 0
    vars = math.factorial(n + k - 1) // (math.factorial(n - 1) * math.factorial(k))
    return vars



