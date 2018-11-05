import sys
from typing import List
import string
import operator


def letter_values(argument: str) -> str:
    letter = argument.lower()
    switcher = {
        "b": "1",
        "f": "1",
        "p": "1",
        "v": "1",
        "c": "2",
        "g": "2",
        "j": "2",
        "k": "2",
        "q": "2",
        "s": "2",
        "x": "2",
        "z": "2",
        "d": "3",
        "t": "3",
        "l": "4",
        "m": "5",
        "n": "5",
        "r": "6"
    }
    return switcher.get(letter)


def convert_to_code(word: str) -> str:
    code = ""
    last_number = ""
    for letter in word:
        converted_letter = letter_values(letter)
        if last_number == converted_letter:
            continue
        last_number = converted_letter
        code += converted_letter
    if len(code) < 3:
        while len(code) != 3:
            code += "0"
    elif len(code) > 3:
        code = code[0:3]
    return code


def remove_letters(word: str) -> str:
    word = word.lower()
    delete_characters = "aeiouyhw"
    translation = str.maketrans("", "", delete_characters)
    word = word.translate(translation)
    return word


def read_buffer(file_stream, buffer_size: int) -> str:
    return file_stream.read(buffer_size)


def is_valid(word: str) -> bool:
    allowed_chars = set(string.ascii_letters)
    return set(word).issubset(allowed_chars)


def is_space_character(character: str) -> bool:
    # These characters will be translated to whitespace or is a whitespace
    space_characters = set([" ", "-", "\\", "&", "#", "\'"])
    return set(character).issubset(space_characters)


def convert_to_soundex(word: str) -> str:
    try:
        if not is_valid(word):
            raise ValueError
        remainder = word[1:]
        if len(remainder) > 0:
            remainder = remove_letters(remainder)
            remainder = convert_to_code(remainder)
            soundex_word = word[0].lower() + remainder
        else:
            soundex_word = word[0].lower() + "000"
        return soundex_word
    except ValueError:
        print("Invalid word")
        return None


def remove_invalid_words(list_of_words: List[str]) -> List[str]:
    new_list = [item for item in list_of_words if is_valid(item)]
    return new_list


def refactor_punctuation(text: str) -> str:
    in_tab = "-\\&#\'/:"  # input table
    out_tab = "       "  # output table
    delete_tab = ",.;\r\n\t()[]<>!?\""
    translation = str.maketrans(in_tab, out_tab, delete_tab)
    return text.translate(translation)


def split_valid_words(text: str) -> List[str]:
    text = refactor_punctuation(text)
    list_of_words = str.split(text, " ")
    list_of_words = [x for x in list_of_words if not x == '']
    list_of_words = remove_invalid_words(list_of_words)
    return list_of_words


def compare_codes(target_word: str, soundex_word: str) -> int:
    score = 0
    for i in range(0, 4):
        if target_word[i] == soundex_word[i]:
            score += 4 - i
    return score


def find_new_minimum(score_table: dict) -> List:
    sorted_table = sorted(score_table.items(), key=operator.itemgetter(1))
    return [sorted_table[0][0], sorted_table[0][1]]


def score_codes(score_table: dict,
                target_word: str,
                list_of_words: List[str],
                known_minimum: List) -> dict:
    for item in list_of_words:
        if item not in score_table:
            soundex_word = convert_to_soundex(item)
            score = compare_codes(target_word, soundex_word)
            if score > known_minimum[1]:
                del score_table[known_minimum[0]]
                score_table[item] = score
                new_minimum = find_new_minimum(score_table)
                known_minimum[0] = new_minimum[0]
                known_minimum[1] = new_minimum[1]
        else:
            continue
    return score_table


def init_score_table() -> dict:
    score_table = {}
    for i in range(0, 5):
        score_table["NaN" + str(i)] = 0
    return score_table


def init_soundex(filename: str, target_word: str, buffer_size: int) -> dict:
        remainder = ""
        score_table = init_score_table()
        known_minimum = find_new_minimum(score_table)
        f = open(filename, "r")
        while True:
            read_text = read_buffer(f, buffer_size)
            if not read_text:
                if remainder != "":
                    # score the last word
                    score_table = score_codes(score_table,
                                              target_word,
                                              list(remainder),
                                              known_minimum)
                break
            if remainder != "":
                flag = is_space_character(read_text[0])
                if not flag:
                    read_text = remainder + read_text
                else:
                    read_text = remainder + " " + read_text
                remainder = ""
            list_of_words = split_valid_words(read_text)
            # buffer doesn't know if the word is complete
            if not is_space_character(read_text[len(read_text)-1]):
                remainder = list_of_words[len(list_of_words)-1]
                list_of_words = list_of_words[0:len(list_of_words)-1]
            score_table = score_codes(score_table, target_word,
                                      list_of_words, known_minimum)
        f.close()
        return score_table


def print_scores(scores: dict):
    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1),
                           reverse=True)
    print("Score \t Word")
    for item in sorted_scores:
        print(repr(item[1]).rjust(5), " \t", repr(item[0]).ljust(0))


if __name__ == '__main__':
    filename = sys.argv[1]
    target_word = convert_to_soundex(sys.argv[2])
    scores = init_soundex(filename, target_word, 255)
    print_scores(scores)
