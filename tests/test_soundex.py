from teso_soundex import soundex
import pytest

def test_return_x():
    assert soundex.return_x(123) == 123
