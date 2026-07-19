"""Tests for string analysis helpers."""

from __future__ import annotations

import pytest

from string_tools import count_vowels, is_palindrome, longest_word


class TestCountVowels:
    def test_normal_case(self) -> None:
        assert count_vowels("hello world") == {"a": 0, "e": 1, "i": 0, "o": 2, "u": 0}

    def test_empty(self) -> None:
        assert count_vowels("") == {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}

    def test_vowels_present(self) -> None:
        assert count_vowels("aeiou") == {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1}

    def test_no_vowels(self) -> None:
        assert count_vowels("rhythm") == {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}

    def test_case_sensitivity(self) -> None:
        assert count_vowels("AaEeIiOoUu") == {"a": 2, "e": 2, "i": 2, "o": 2, "u": 2}


class TestLongestWord:
    def test_typical(self) -> None:
        assert longest_word("the quick brown fox") == "quick"

    def test_tie_breaker(self) -> None:
        assert longest_word("cat dog bat") == "cat"

    def test_empty_string(self) -> None:
        assert longest_word("") is None

    def test_spaces(self) -> None:
        assert longest_word("   ") is None

    def test_single(self) -> None:
        assert longest_word("hello") == "hello"


class TestIsPalindrome:
    @pytest.mark.parametrize(
        "text,expected",
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
    def test_parametrized(self, text: str, expected: bool) -> None:
        assert is_palindrome(text) == expected

    def test_punctuation(self) -> None:
        assert is_palindrome("Madam, I'm Adam.") is True

    def test_monochar(self) -> None:
        assert is_palindrome("aaaa") is True