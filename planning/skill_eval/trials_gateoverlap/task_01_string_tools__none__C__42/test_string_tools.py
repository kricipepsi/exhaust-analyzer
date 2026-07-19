from string_tools import count_vowels, longest_word


def test_count_vowels():
    assert count_vowels("hello") == {"a": 0, "e": 1, "i": 0, "o": 0, "u": 0}


def test_longest_word():
    assert longest_word("the quick brown fox") == "quick"
