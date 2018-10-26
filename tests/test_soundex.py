from teso_soundex import soundex
import pytest

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
