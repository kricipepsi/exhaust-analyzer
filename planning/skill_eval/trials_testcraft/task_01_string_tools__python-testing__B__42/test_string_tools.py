from __future__ import annotations

import pytest
from string_tools import count_vowels, is_palindrome, longest_word


class TestCountVowels:
    def test_normal_text(self) -> None:
        assert count_vowels("Hello World") == {"a": 0, "e": 1, "i": 0, "o": 2, "u": 0}

    def test_case_insensitive(self) -> None:
        assert count_vowels("AaEeIiOoUu") == {"a": 2, "e": 2, "i": 2, "o": 2, "u": 2}

    def test_empty_input(self) -> None:
        assert count_vowels("") == {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}

    def test_no_vowels(self) -> None:
        assert count_vowels("rhythm") == {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}


class TestLongestWord:
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("the quick brown fox jumps", "quick"),
            ("cat dog bat", "cat"),
            ("singleword", "singleword"),
            ("aa bb cc", "aa"),
        ],
    )
    def test_returns_first_longest(self, text: str, expected: str) -> None:
        assert longest_word(text) == expected

    def test_empty_returns_none(self) -> None:
        assert longest_word("") is None

    def test_whitespace_only_returns_none(self) -> None:
        assert longest_word("   \t\n ") is None


class TestIsPalindrome:
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("racecar", True),
            ("A man a plan a canal Panama", True),
            ("No lemon, no melon", True),
            ("hello", False),
            ("ab", False),
            ("a", True),
            ("", True),
        ],
    )
    def test_palindrome_cases(self, text: str, expected: bool) -> None:
        assert is_palindrome(text) == expected
