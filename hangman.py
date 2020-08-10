#########################################################
#FILE : hangman.py
#WRITER : Joel Yeger, joelyeger
#EXERCISE : intro2cs2 ex4 2020
#DESCRIPTION : A game of hangman
#STUDENTS I DISCUSSED THE EXERCISE WITH: none
#WEB PAGES I USED: none
#########################################################

import hangman_helper

INVALID_INPUT = "Invalid input"
LETTER_CHOSEN = "Letter has already been chosen"
WIN = "You win!"
LOSE = "You lose! "
GOOD_LUCK = "Good luck!"
YOUR_TURN = " This is your time to play"
SORRY = "Sorry this isn't the word"


def update_word_pattern(word,pattern,letter):
    """updates the pattern acorrding to the given word"""
    num_index = 0
    if letter in word:
        word_list = list(word)
        pattern_list = list(pattern)

        while num_index <= word.rfind(letter):
                num_index = word.index(letter, num_index)
                pattern_list[num_index] = word_list[num_index]
                num_index = num_index + 1


        return ''.join(pattern_list)
    else:
        return pattern

def check_letter(letter,wrong_guess_list,pattern,word):
    """checks all possible inputs of letters and returns a number
     accordingly"""
    if len(letter) == 1 and letter.islower():
        if letter in wrong_guess_list or letter in pattern:
            return 1

        elif pattern == update_word_pattern(word, pattern,
                                            letter):
            return 2

        elif letter in word:
            return 3

    else: return 0

def check_list(list,tat_list):
    """returns a list of words in the length of HINT_LENGTH or less"""
    count = 1
    if len(list) > hangman_helper.HINT_LENGTH:
        while len(tat_list) != hangman_helper.HINT_LENGTH:
            if count < hangman_helper.HINT_LENGTH:
                try:
                    tat_list.append(list[len(list) * count //
                                               hangman_helper.HINT_LENGTH])
                    count += 1
                except:
                    break
    else:
        tat_list = list
    return tat_list


def run_single_game(words_list, score):
    """operating one game of hangman"""
    word = hangman_helper.get_random_word(words_list)
    wrong_guess_list = []
    correct_guess_list = []
    pattern = len(word) * '_'
    if score > 0:
        hangman_helper.display_state(pattern, wrong_guess_list, score,
                                 GOOD_LUCK)
    input_num = 0
    while pattern != word and score > 0 and input_num < 26:
        user_input = hangman_helper.get_input()
        if hangman_helper.LETTER == user_input[0]:
            check_let = check_letter(user_input[1],
                                     wrong_guess_list, pattern, word)
            if check_let == 1:
                hangman_helper.display_state(pattern,wrong_guess_list,
                                                 score,INVALID_INPUT)

            elif check_let == 2:
                    wrong_guess_list.append(user_input[1])
                    score -= 1
                    if score == 0 :
                        break
                    input_num += 1
                    hangman_helper.display_state(pattern,wrong_guess_list,
                                        score,LETTER_CHOSEN)

            elif check_let == 3 :
                score -= 1
                pattern = update_word_pattern(word, pattern, user_input[1])
                count_letter = pattern.count(user_input[1])
                score += count_letter*(count_letter+1) // 2
                correct_guess_list.append(user_input[1])
                input_num += 1
                if pattern == word:
                    break

                hangman_helper.display_state(pattern,wrong_guess_list,score,
                                                  YOUR_TURN)

            elif check_let == 0:
                hangman_helper.display_state(pattern, wrong_guess_list,
                                             score, INVALID_INPUT)

        elif hangman_helper.WORD == user_input[0]:
            score -= 1
            if user_input[1] == word:
                missing_letters = pattern.count('_')
                score += missing_letters*(missing_letters+1) // 2
                pattern = word
                break

            elif score == 0:
                break
            else:
                hangman_helper.display_state(pattern, wrong_guess_list,
                                             score,SORRY + YOUR_TURN)


        elif hangman_helper.HINT == user_input[0]:
            score -= 1
            matches = filter_words_list(words_list,pattern,wrong_guess_list)
            tat_matches = [matches[0]]
            tat_matches = check_list(matches,tat_matches)
            hangman_helper.show_suggestions(tat_matches)
            if score == 0:
                break

        else:
            score -= 1
            if score == 0 :
                break
            hangman_helper.display_state(pattern,wrong_guess_list,score,
                                         INVALID_INPUT)


    if score == 0:
        hangman_helper.display_state(pattern, wrong_guess_list, score,
                                     LOSE+word)
    else:
        hangman_helper.display_state(pattern, wrong_guess_list, score,
                                     WIN)


    return score



def main():
    """operate several games of hangman acorrding to user will"""
    words_list = list(hangman_helper.load_words())
    game_played = 1
    score = run_single_game(words_list, hangman_helper.POINTS_INITIAL)
    another_game = True
    while another_game:
        if score > 0:
            another_game =  hangman_helper.play_again("Games played: " +
                                                      str(game_played) +
                                                      " current score: " +
                                                      str(score) +
                                                      " would you like"
                                                      " to play again?")


            if another_game == False:
                break
            score = run_single_game(words_list,score)
            game_played += 1

        elif score == 0:
            another_game = hangman_helper.play_again("Games played: " +
                                                     str(game_played) +
                                                     " would you like to "
                                                     "restart the game?")
            if another_game == False:
                break
            score = run_single_game(words_list, hangman_helper.POINTS_INITIAL)
            game_played = 1







def filter_words_list(words, pattern, wrong_guess_lst):
    """returns a list of optional words acorrding to pattern and wrong
    guess list"""

    hint_list = []
    pattern_count = len(pattern) - pattern.count('_')

    for word in words:
        error_count = 0
        word_count = 0
        for let in wrong_guess_lst:
            if let in word:
                error_count += 1
        if error_count > 0:
            continue
        elif len(word) == len(pattern):
            for parameter in pattern:
                if parameter == '_':
                    continue
                elif parameter in word:
                    if word[pattern.index(parameter)] == parameter:
                        if word.count(parameter) == pattern.count(parameter):
                            word_count +=1
                        else:
                            break
                    else:
                        break
                else:
                    break
        else:
            continue
        if word_count == pattern_count:
            hint_list.append(word)
    return hint_list

if __name__ == '__main__':
    main()
















