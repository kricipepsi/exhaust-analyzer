from __future__ import annotations

import pytest
from string_tools import count_vowels, is_palindrome, longest_word


class DescribeCountVowels:
    def test_normal_text(self) -> None:
        result = count_vowels("Hello World")
        assert result == {"a": 0, "e": 1, "i": 0, "o": 2, "u": 0}

    def test_case_insensitive(self) -> None:
        result = count_vowels("AaEeIiOoUu")
        assert result == {"a": 2, "e": 2, "i": 2, "o": 2, "u": 2}

    def test_empty_string(self) -> None:
        result = count_vowels("")
        assert result == {v: 0 for v in "aeiou"}

    def test_no_vowels(self) -> None:
        result = count_vowels("rhythm")
        assert all(v == 0 for v in result.values())


class DescribeLongestWord:
    def test_basic(self) -> None:
        assert longest_word("the quick brown fox jumps") == "quick"

    def test_tie_returns_first(self) -> None:
        assert longest_word("cat dog bat") == "cat"

    def test_empty_returns_none(self) -> None:
        assert longest_word("") is None

    def test_whitespace_only(self) -> None:
        assert longest_word("   ") is None


class DescribeIsPalindrome:
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("racecar", True),
            ("A man a plan a canal Panama", True),
            ("hello", False),
            ("", True),
            ("a", True),
            ("No lemon, no melon", True),
            ("ab", False),
        ],
    )
    def test_cases(self, text: str, expected: bool) -> None:
        assert is_palindrome(text) == expected
