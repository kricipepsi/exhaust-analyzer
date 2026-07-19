from __future__ import annotations

import pytest
from string_tools import count_vowels, is_palindrome, longest_word


class TestCountVowels:
    def test_normal_text(self) -> None:
        assert count_vowels("Hello World") == {"a": 0, "e": 1, "i": 0, "o": 2, "u": 0}

    def test_case_insensitive(self) -> None:
        assert count_vowels("AaEeIiOoUu") == {"a": 2, "e": 2, "i": 2, "o": 2, "u": 2}

    def test_empty(self) -> None:
        assert count_vowels("") == {v: 0 for v in "aeiou"}


class TestLongestWord:
    def test_basic(self) -> None:
        assert longest_word("the quick brown") == "quick"

    def test_tie_first(self) -> None:
        assert longest_word("cat dog bat") == "cat"

    def test_empty(self) -> None:
        assert longest_word("") is None


class TestIsPalindrome:
    @pytest.mark.parametrize("text,expected", [
        ("racecar", True),
        ("A man a plan a canal Panama", True),
        ("hello", False),
        ("", True),
    ])
    def test_cases(self, text: str, expected: bool) -> None:
        assert is_palindrome(text) == expected
