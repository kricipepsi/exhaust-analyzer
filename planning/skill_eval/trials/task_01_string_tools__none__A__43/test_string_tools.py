"""Tests for string_tools."""

from __future__ import annotations

import pytest

from string_tools import count_vowels, is_palindrome, longest_word


class TestCountVowels:
    def test_typical_input(self) -> None:
        assert count_vowels("hello world") == {"a": 0, "e": 1, "i": 0, "o": 2, "u": 0}

    def test_empty_input(self) -> None:
        assert count_vowels("") == {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}

    def test_only_vowels(self) -> None:
        assert count_vowels("aeiou") == {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1}

    def test_only_consonants(self) -> None:
        assert count_vowels("rhythm") == {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}

    def test_mixed_case(self) -> None:
        assert count_vowels("AaEeIiOoUu") == {"a": 2, "e": 2, "i": 2, "o": 2, "u": 2}


class TestLongestWord:
    def test_basic(self) -> None:
        assert longest_word("the quick brown fox") == "quick"

    def test_tiebreaker(self) -> None:
        assert longest_word("cat dog bat") == "cat"

    def test_empty_string_returns_none(self) -> None:
        assert longest_word("") is None

    def test_whitespace_returns_none(self) -> None:
        assert longest_word("   ") is None

    def test_one_word(self) -> None:
        assert longest_word("solo") == "solo"


class TestIsPalindrome:
    @pytest.mark.parametrize(
        "candidate,expected",
        [
            ("racecar", True),
            ("hello", False),
            ("", True),
            ("a", True),
            ("A man a plan a canal Panama", True),
            ("No lemon no melon", True),
            ("not a palindrome", False),
        ],
    )
    def test_parametrized(self, candidate: str, expected: bool) -> None:
        assert is_palindrome(candidate) == expected

    def test_ignores_punctuation_and_case(self) -> None:
        assert is_palindrome("Madam, I'm Adam.") is True

    def test_all_identical_characters(self) -> None:
        assert is_palindrome("aaaa") is True