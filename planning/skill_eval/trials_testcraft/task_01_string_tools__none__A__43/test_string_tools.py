from string_tools import count_vowels, is_palindrome, longest_word


def test_count_vowels():
    assert count_vowels("Hello World") == {"a": 0, "e": 1, "i": 0, "o": 2, "u": 0}


def test_longest_word():
    assert longest_word("the quick brown fox") == "quick"


def test_is_palindrome():
    assert is_palindrome("racecar") is True
