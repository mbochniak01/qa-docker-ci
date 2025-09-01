from app.text_utils import clean_text


def test_basic_sentence():
    assert clean_text("Hello, World!") == "hello world"


def test_multiple_spaces():
    assert clean_text("Hello     World") == "hello world"


def test_numbers_and_text():
    assert clean_text("Python 3.11 >>> rocks!!!") == "python 311 rocks"


def test_empty_string():
    assert clean_text("") == ""


def test_only_punctuation():
    assert clean_text("!!!???") == ""
