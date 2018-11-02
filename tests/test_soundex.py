from teso_soundex import soundex
# import pytest

fixtures_folder = 'tests/fixtures/'


def test_read_buffer_can_read_first_10_bytes():
    with open(fixtures_folder + 'test_text.txt') as f:
        read_text = soundex.read_buffer(f, 10)
        assert read_text == "I want to "


def test_read_buffer_can_read_whole_file():
    whole_text = ""
    with open(fixtures_folder + 'test_text.txt') as f:
        while True:
            read_text = soundex.read_buffer(f, 10)
            if not read_text:
                break
            whole_text += read_text
        assert whole_text == "I want to scream, but I have no mouth\n"


def test_convert_soundex_can_accurately_convert():
    converted_word = soundex.convert_to_soundex("litttuania")
    assert converted_word == "l350"


def test_split_words_by_spaces():
    with open(fixtures_folder + 'test_text.txt') as f:
        read_text = soundex.read_buffer(f, 255)
        split_words = soundex.split_valid_words(read_text)
        assertion_list = ["I", "want", "to", "scream",
                          "but", "I", "have", "no", "mouth"]
        assert split_words == assertion_list


def test_check_validity_of_words():
    words = ["foo", "bar", "foobar", "LOWERCASEuppercase", "100platypuses",
             "D0decahedron", "l33t", "#~Unkown~#@^symbols%"]
    valid_words = ["foo", "bar", "foobar", "LOWERCASEuppercase"]
    words = soundex.remove_invalid_words(words)
    assert words == valid_words


def test_read_and_convert_to_soundex():
    assertion_list = ["i000", "w530", "t000", "s265",
                      "b300", "i000", "h100", "n000", "m300"]
    with open(fixtures_folder + "test_text.txt") as f:
        read_text = soundex.read_buffer(f, 255)
        list_of_words = soundex.split_valid_words(read_text)
        soundex_list = []
        for word in list_of_words:
            soundex_word = soundex.convert_to_soundex(word)
            soundex_list.append(soundex_word)
        assert assertion_list == soundex_list
