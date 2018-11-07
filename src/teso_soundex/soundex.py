import sys
from typing import List
import string
import operator
import os.path

# ---------------------------------------
# Defines
# ---------------------------------------

# set of allowed characters
ALLOWED_CHARACTERS = set(string.ascii_letters)

_in_tab = "-\\&#\'/:\""  # input table
_out_tab = "        "  # output table
_delete_tab = ",.;\r\n\t()[]<>!?"

# Translation table for punctuation symbols and escape characters
PUNCTUATION_TABLE = str.maketrans(_in_tab, _out_tab, _delete_tab)

_delete_characters = "aeiouyhw"

# Letters to delete for soundex conversion
DELETE_CHARACTERS_TABLE = str.maketrans("", "", _delete_characters)

# Characters that are translated to whitespace
SPACE_CHARACTERS = set([" ", "-", "\\", "&", "#", "\'", "\"", "/", ":"])

LETTER_VALUES = {
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

# ---------------------------------------
# Conversion to soundex functions
# ---------------------------------------


def convert_to_soundex(word: str) -> str:
    """Converts given word to Soundex code"""
    remainder = word[1:]
    if len(remainder) > 0:
        remainder = remove_letters(remainder)
        remainder = convert_to_code(remainder)
        soundex_word = word[0].lower() + remainder
    else:
        soundex_word = word[0].lower() + "000"
    return soundex_word


def convert_to_code(word: str) -> str:
    """Converts remainder to Soundex code and returns it"""
    code = ""
    last_number = ""
    for letter in word:
        converted_letter = LETTER_VALUES.get(letter)
        if last_number == converted_letter:
            continue
        last_number = converted_letter
        code += converted_letter
    while len(code) < 3:
        code += "0"
    return code[0:3]


def remove_letters(word: str) -> str:
    """Removes unnecessary letters for Soundex algorithm"""
    word = word.lower()
    word = word.translate(DELETE_CHARACTERS_TABLE)
    return word

# ---------------------------------------
# String parsing functions
# ---------------------------------------


def split_valid_words(text: str) -> List[str]:
    """Parses given text into a list of valid words"""
    text = refactor_punctuation(text)
    list_of_words = [x for x in str.split(text, " ")
                     if not x == '' and is_valid_word(x)]
    return list_of_words


def refactor_punctuation(text: str) -> str:
    """Translates found punctuation symbols"""
    return text.translate(PUNCTUATION_TABLE)

# ---------------------------------------
# Validation functions
# ---------------------------------------


def is_valid_word(word: str) -> bool:
    """Check if the word is valid and consists only ascii characters"""
    return set(word).issubset(ALLOWED_CHARACTERS)


def is_space_character(symbol: str) -> bool:
    """Checks if the character is (or soon to be) whitespace"""
    return set(symbol).issubset(SPACE_CHARACTERS)


def check_for_valid_input():
    """Checks user inputs and in case of fail, aborts execution"""
    if sys.argv[1] == "--help":
        print("python soundex.py <path/to/file> <target_word>")
        quit()
    elif len(sys.argv) < 3:
        print_error("Not enough arguments, please use --help")
        quit()
    elif not os.path.isfile(sys.argv[1]):
        print_error("File doesn't exist or invalid path")
        quit()
    elif not is_valid_word(sys.argv[2]):
        print_error("Invalid target word")
        quit()

# ---------------------------------------
# Score Table functions
# ---------------------------------------


def score_codes(score_table: dict, target: str,
                list_of_words: List[str], known_minimum: List) -> dict:
    """Checks the score of found words and returns a dictionary of top words"""
    for item in list_of_words:
        if item not in score_table:
            soundex_word = convert_to_soundex(item)
            score = compare_codes(target, soundex_word)
            if score > known_minimum[1]:
                del score_table[known_minimum[0]]
                score_table[item] = score
                known_minimum[0:1] = find_new_minimum(score_table)
        else:
            continue
    return score_table


def compare_codes(target: str, soundex_word: str) -> int:
    """Compares two soundex words and returns the score"""
    score = 0
    for i in range(0, 4):
        if target[i] == soundex_word[i]:
            score += 4 - i
    return score


def find_new_minimum(score_table: dict) -> List:
    """Finds the minimum value in the dict, and returns in form a of a list"""
    sorted_table = sorted(score_table.items(), key=operator.itemgetter(1))
    return [sorted_table[0][0], sorted_table[0][1]]


def init_score_table() -> dict:
    """Initializes score table, filling with 5 empty words"""
    score_table = {}
    for i in range(0, 5):
        score_table["NaN" + str(i)] = 0
    return score_table


# ---------------------------------------
# Input functions
# ---------------------------------------

def buffer_read(file_stream, buffer_size: int) -> str:
    """Reads a given amount of characters from a file"""
    return file_stream.read(buffer_size)

# ---------------------------------------
# Output functions
# ---------------------------------------


def print_scores(scores: dict):
    """Prints scores in a formated table"""
    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1),
                           reverse=True)
    print("Score \t Word")
    for item in sorted_scores:
        print(repr(item[1]).rjust(5), " \t", repr(item[0]).ljust(0))


def print_error(*args, **kwargs):
        """Prints error in stderr"""
        print(*args, file=sys.stderr, **kwargs)

# ---------------------------------------
# Main functions
# ---------------------------------------


def init_soundex(filepath: str, target_word: str, buffer_size: int) -> dict:
    """Parses given file and returns a dict of top 5 matched soundex words"""
    remainder = ""
    score_table = init_score_table()
    known_minimum = find_new_minimum(score_table)
    f = open(filepath, "r", encoding="UTF-8")
    while True:
        read_text = buffer_read(f, buffer_size)
        if not read_text:
            if remainder != "":
                # score the last word
                score_table = score_codes(score_table, target_word,
                                          [remainder], known_minimum)
            break

        # add remainder to the beginning of read_text
        if remainder != "":
            # flag determines if the character is a (or soon to be) space
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


if __name__ == '__main__':
    check_for_valid_input()
    filepath = sys.argv[1]
    soundex_word = convert_to_soundex(sys.argv[2])
    scores = init_soundex(filepath, soundex_word, 1024)
    print_scores(scores)
