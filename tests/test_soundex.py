from typing import List
from teso_soundex import soundex
# import pytest

fixtures_folder = 'tests/fixtures/'


# ---------------------------------------
# Helper Functions
# ---------------------------------------

def get_full_word_list(file_stream) -> List[str]:
    remainder = ""
    word_list = []
    while True:
        read_text = soundex.buffer_read(file_stream, 255)
        if not read_text:
            break
        if remainder != "":
            flag = soundex.is_space_character(read_text[0])
            if not flag:
                read_text = remainder + read_text
            else:
                read_text = remainder + " " + read_text
            remainder = ""
        list_of_words = soundex.split_valid_words(read_text)
        if not soundex.is_space_character(read_text[len(read_text)-1]):
            remainder = list_of_words[len(list_of_words)-1]
            list_of_words = list_of_words[0:len(list_of_words)-1]
        word_list += list_of_words
    word_list.append(remainder)
    return word_list


# ---------------------------------------
# Tests
# ---------------------------------------

def test_buffer_read_can_read_first_10_bytes():
    with open(fixtures_folder + 'test_text.txt',
              encoding="UTF-8") as f:
        read_text = soundex.buffer_read(f, 10)
        assert read_text == "I want to "


def test_buffer_read_can_read_whole_file():
    whole_text = ""
    with open(fixtures_folder + 'test_text.txt',
              encoding="UTF-8") as f:
        while True:
            read_text = soundex.buffer_read(f, 10)
            if not read_text:
                break
            whole_text += read_text
        assert whole_text == "I want to scream, but I have no mouth\n"


def test_convert_soundex_can_accurately_convert():
    converted_word = soundex.convert_to_soundex("litttuania")
    assert converted_word == "l350"


def test_split_words_by_spaces():
    with open(fixtures_folder + 'test_text.txt',
              encoding="UTF-8") as f:
        read_text = soundex.buffer_read(f, 255)
        split_words = soundex.split_valid_words(read_text)
        assertion_list = ["I", "want", "to", "scream",
                          "but", "I", "have", "no", "mouth"]
        assert split_words == assertion_list


def test_check_validity_of_words():
    words = ("foo bar foobar LOWERCASEuppercase 100platypuses"
             "D0decahedron l33t #~Unkown~#@^symbols%")
    valid_words = ["foo", "bar", "foobar", "LOWERCASEuppercase"]
    words = soundex.split_valid_words(words)
    assert words == valid_words


def test_read_and_convert_to_soundex():
    assertion_list = ["i000", "w530", "t000", "s265",
                      "b300", "i000", "h100", "n000", "m300"]
    with open(fixtures_folder + "test_text.txt",
              encoding="UTF-8") as f:
        read_text = soundex.buffer_read(f, 255)
        list_of_words = soundex.split_valid_words(read_text)
        soundex_list = []
        for word in list_of_words:
            soundex_word = soundex.convert_to_soundex(word)
            soundex_list.append(soundex_word)
        assert assertion_list == soundex_list


def test_reading_file_in_buffer_and_converting_to_soundex():
    with open(fixtures_folder + "test_bigger_text.txt",
              encoding="UTF-8") as f:
        f2 = open(fixtures_folder + "test_soundex_bigger_text.txt")
        read_assertion = soundex.buffer_read(f2, 20000)
        assertion = read_assertion.split(" ")
        word_list = get_full_word_list(f)
        print(word_list)
        soundex_list = []
        for word in word_list:
            soundex_word = soundex.convert_to_soundex(word)
            soundex_list.append(soundex_word)
        f2.close()
        assert soundex_list == assertion


def test_scoring_of_code():
    target_word = "l350"
    score_table = soundex.init_score_table()
    known_minimum = soundex.find_new_minimum(score_table)
    with open(fixtures_folder + "test_wiki_lt.txt",
              encoding="UTF-8") as f:
        word_list = get_full_word_list(f)
        score_table = soundex.score_codes(score_table, target_word,
                                          word_list, known_minimum)
        assert score_table["Lithuania"] == 10


def test_minimum_finding():
    score_table = {"foo": 5, "bar": 2, "foobar": 7}
    new_minimum = soundex.find_new_minimum(score_table)
    assert new_minimum == ["bar", 2]
