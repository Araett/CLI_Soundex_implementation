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


'''
test_reading_file_in_buffer_and_converting_to_soundex()
The code is similar to soundex.init_soundex(), due the fact,
the function doesn't return anything
'''


def test_reading_file_in_buffer_and_converting_to_soundex():
    with open(fixtures_folder + "test_bigger_text.txt") as f:
        f2 = open(fixtures_folder + "test_soundex_bigger_text.txt")
        read_assertion = soundex.read_buffer(f2, 20000)
        assertion = read_assertion.split(" ")
        remainder = ""
        soundex_list = []
        while True:
            read_text = soundex.read_buffer(f, 25)
            if not read_text:
                if remainder != "":
                    soundex_word = soundex.convert_to_soundex(remainder)
                    soundex_list.append(soundex_word)
                break
            if remainder != "":
                flag = soundex.is_space_character(read_text[0])
                if not flag:
                    read_text = remainder + read_text
                else:
                    read_text = remainder + " " + read_text
                remainder = ""
            print(read_text)
            list_of_words = soundex.split_valid_words(read_text)
            if not soundex.is_space_character(read_text[len(read_text)-1]):
                remainder = list_of_words[len(list_of_words)-1]
                list_of_words = list_of_words[0:len(list_of_words)-1]
            print(list_of_words)
            for word in list_of_words:
                soundex_word = soundex.convert_to_soundex(word)
                soundex_list.append(soundex_word)
        print(soundex_list)
        assert soundex_list == assertion


'''def create_test_file_with_soundex():
    with open(fixtures_folder + "test_bigger_text.txt") as f:
        w = open(fixtures_folder + "test_soundex_bigger_text.txt", "w")
        read_text = soundex.read_buffer(f, 200000)
        list_of_words = soundex.split_valid_words(read_text)
        soundex_list = []
        for word in list_of_words:
            print(word)
            soundex_word = soundex.convert_to_soundex(word)
            soundex_list.append(soundex_word)
        test_to_write = ""
        for item in soundex_list:
            test_to_write += item + " "
        w.write(test_to_write)
        w.close()
        assert True'''
