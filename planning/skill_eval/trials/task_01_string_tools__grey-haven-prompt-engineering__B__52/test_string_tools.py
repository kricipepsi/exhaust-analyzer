"""Tests for string_tools module."""

from __future__ import annotations

import pytest

from string_tools import count_vowels, is_palindrome, longest_word


class TestCountVowels:
    def test_basic(self) -> None:
        result = count_vowels("hello world")
        assert result == {"a": 0, "e": 1, "i": 0, "o": 2, "u": 0}

    def test_empty_string(self) -> None:
        assert count_vowels("") == {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}

    def test_all_five_vowels(self) -> None:
        assert count_vowels("aeiou") == {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1}

    def test_only_consonants(self) -> None:
        result = count_vowels("rhythm")
        assert result == {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}

    def test_case_insensitive(self) -> None:
        result = count_vowels("AaEeIiOoUu")
        assert result == {"a": 2, "e": 2, "i": 2, "o": 2, "u": 2}


class TestLongestWord:
    def test_basic(self) -> None:
        assert longest_word("the quick brown fox") == "quick"

    def test_tie_first_wins(self) -> None:
        assert longest_word("cat dog bat") == "cat"

    def test_empty_string(self) -> None:
        assert longest_word("") is None

    def test_only_spaces(self) -> None:
        assert longest_word("   ") is None

    def test_one_word(self) -> None:
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
    def test_palindromes(self, text: str, expected: bool) -> None:
        assert is_palindrome(text) == expected

    def test_punctuation_and_case_ignored(self) -> None:
        assert is_palindrome("Madam, I'm Adam.") is True

    def test_all_same_letter(self) -> None:
        assert is_palindrome("aaaa") is True