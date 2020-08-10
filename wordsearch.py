#Porgram which find words inside a matrix

from copy import deepcopy

import sys, os




#files related functions:

def read_wordlist_file(filename):
    """returns a list of words out of a file"""
    words_file = open(filename)
    words = words_file.read().splitlines()
    words_file.close()
    return words


def read_matrix_file(filename):
    """returns a list of lists of letters"""
    matrix_file = open(filename)

    final_matrix = [i.strip().split(",") for i in matrix_file]
    matrix_file.close()
    return final_matrix


def write_output_file(resaults, output_filename):
    """creats a file with the resualts"""
    out_put_file = open(output_filename, 'w')
    new_resaults = unpack_list_of_tuples(resaults)
    reasults = out_put_file.write("\n".join(new_resaults))
    out_put_file.close()





#functions asked in the exercise instruction:


def find_words_in_matrix(word_list, matrix, directions):
    """returns a list of tupels which inform the amount of apearences
    of each word in the matrix"""

    list_of_resaults = letter_to_correct_search(directions, word_list, matrix)
    unpacked_list_of_resaults = unpack_lists(list_of_resaults)
    final_resaults_not_sorted = final_resault(unpacked_list_of_resaults)
    final_resalt = sort_resault_as_initial_list(final_resaults_not_sorted,
                                                word_list)
    return final_resalt



def main_func():
    """use all the functions of the ex"""
    input = sys.argv[1:]
    if check_input_args(input) is None:
        words = read_wordlist_file(input[0])
        matrix = read_matrix_file(input[1])
        resaults = find_words_in_matrix(words, matrix, input[3])
        write_output_file(resaults, input[2])
    else:
        print(check_input_args(input))



def check_input_args(args):
    """checks if the arguments are valid"""
    count = 0
    directions = ['w','d','r','l','u','x','y','z']

    if len(args) == 4:
        for i in args[3]:
            if i not in directions:
                return "You did not enter a valid direction order"

    if len(args) != 4:
        return "You have entered an invalid number of argumnets"

    else:
        if os.path.isfile(args[0]) and os.path.isfile(args[1]):
            return None
        else:
            return "You entered an invalid word filename"











#matrix searching related functions:


def letter_to_correct_search(directions, word_list, matrix):
    """match a letter to the wanted search direction"""
    u, d, r, l, w, x, y, z = [], [], [], [], [], [], [], []
    if 'u' in directions: u.append(search_up(word_list, matrix))
    if 'd' in directions: d.append(search_down(word_list, matrix))
    if 'r' in directions: r.append(search_right(word_list, matrix))
    if 'l' in directions: l.append(search_left(word_list, matrix))
    if 'w' in directions: w.append(diagonal_up_right(word_list, matrix))
    if 'x' in directions: x.append(diagonal_up_left(word_list, matrix))
    if 'y' in directions: y.append(diagonal_down_right(word_list, matrix))
    if 'z' in directions: z.append(diagonal_down_left(word_list, matrix))
    return [u, d, r, l, w, x, y, z]


def search_right(words, matrix):
    """returns a list of words"""
    list_of_words = []
    temp_mat = deepcopy(matrix)
    for i in temp_mat:
        str = "".join(i)
        indicator = len(str) + 1
        for k in range(indicator):
            for j in range(k, indicator):
                if j > k:
                    if str[k:j] in words:
                        list_of_words.append(str[k:j])


    return list_of_words



def search_left(words,matrix):
    """returns a list of words"""
    temp_mat = revers_matrix(matrix)
    return search_right(words, temp_mat)


def search_down(words, matrix):
    """returns a list of words"""
    temp_mat = sort_mat_from_down_to_right(matrix)
    return search_right(words, temp_mat)


def search_up(words, matrix):
    """returns a list of words"""
    temp_mat = mat_up_side_down(matrix)
    return search_down(words, temp_mat)


def diagonal_down_right(words, matrix):
    """returns a list of words"""
    new_mat = sort_diaganol_down_right(matrix)
    return search_right(words, new_mat)


def diagonal_down_left(words, matrix):
    """returns a list of words"""
    new_mat = revers_matrix(matrix)
    return diagonal_down_right(words, new_mat)


def diagonal_up_right(words, matrix):
    """returns a list of words"""
    temp_mat = mat_up_side_down(matrix)
    return diagonal_down_right(words, temp_mat)


def diagonal_up_left(words, matrix):
    """returns a list of words"""
    temp_mat = mat_up_side_down(matrix)
    return diagonal_down_left(words, temp_mat)







#matrix sorting related functions:

def revers_matrix(matrix):
    """returns a reversed matrix"""
    copy_mat = deepcopy(matrix)
    temp_mat = []
    for i in copy_mat:
        i = i[-1::-1]
        temp_mat.append(i)
    return temp_mat

def mat_up_side_down(matrix):
    """returns an upside down matrix"""
    temp_mat = []
    for i in (range(1,len(matrix)+1)):
        temp_mat.append(matrix[-i])
    return temp_mat




def sort_diaganol_down_right(matrix):
    """returrns a matrix sorted as diagonal down right"""
    if matrix == []:
        return []
    else:
         copy_mat = deepcopy(matrix)
         word = []
         temp_mat = []
         new_word = []
         for i in range(len(copy_mat[0])):
            count = i
            for j in copy_mat:
                try:
                    word.append(j[count])
                    count += 1
                except:
                    break
                temp_mat.append(word)
                word = []
         word = []
         for k in range(1, len(copy_mat)):
            new_count = 0
            for t in copy_mat[k:]:
                new_word.append(t[new_count])
                new_count += 1
            temp_mat.append(new_word)
            new_word = []


         return temp_mat


def mat_minus_first_row(matrix):
    """returns a matrix without the first row"""
    if len(matrix) > 1:
        matrix = matrix[1:]
        return matrix
    else: return []


def sort_mat_from_down_to_right(matrix):
    """sort a matrix so you will be able to read it from left to right
    and not up to down"""
    temp_mat = []
    for i in range(len(matrix[0])):
        row = []
        for j in matrix:
            row.append(j[i])
        temp_mat.append(row)
        row = 0
    return temp_mat






#resault related functions:


def unpack_lists(lst):
    """get a list of word out of list of lists of words"""
    temp_resaults = []
    final_resault = []
    for lsts in lst:
        for word in lsts:
            temp_resaults.append(word)

    for word_or_list in temp_resaults:
        try:
            word_or_list.append("testing_object")
            word_or_list.remove("testing_object")
            for words in word_or_list:
                final_resault.append(words)
        except:
            final_resault.append(word_or_list)
    return final_resault




def final_resault(lst):
    """returns a list of tuples"""
    resault = []
    for i in lst:
        count = lst.count(i)
        resault.append((i, count))
    resault = list(set(resault))
    return resault



def sort_resault_as_initial_list(resaults, initial_list):
    """sorts the resault list the same order as the inital words list"""
    sorted_resault_list = []
    for i in initial_list:
        for j in resaults:
            if i in j:
                sorted_resault_list.append(j)
                break

    return sorted_resault_list

def unpack_list_of_tuples(lst):
    """returns a list of strings of the pairs which were in a tuple"""
    new_resault_list = []
    for i in lst:
        word = str(i[0]) + "," + str(i[1])
        new_resault_list.append(word)
    return new_resault_list

if __name__ == '__main__':
    main_func()


