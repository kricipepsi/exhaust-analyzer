from string_tools import count_vowels, is_palindrome


def test_count_vowels():
    assert count_vowels("aeiou") == {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1}


def test_is_palindrome():
    assert is_palindrome("racecar") is True
