"""Tests for text analysis helpers."""

from __future__ import annotations

import pytest

from string_tools import count_vowels, is_palindrome, longest_word


class TestCountVowels:
    def test_basic_text(self) -> None:
        got = count_vowels("hello world")
        want = {"a": 0, "e": 1, "i": 0, "o": 2, "u": 0}
        assert got == want

    def test_empty(self) -> None:
        got = count_vowels("")
        want = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
        assert got == want

    def test_vowels_only(self) -> None:
        assert count_vowels("aeiou") == {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1}

    def test_consonants_only(self) -> None:
        assert count_vowels("rhythm") == {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}

    def test_case_insensitivity(self) -> None:
        got = count_vowels("AaEeIiOoUu")
        want = {"a": 2, "e": 2, "i": 2, "o": 2, "u": 2}
        assert got == want


class TestLongestWord:
    def test_typical(self) -> None:
        assert longest_word("the quick brown fox") == "quick"

    def test_tie_goes_to_first(self) -> None:
        assert longest_word("cat dog bat") == "cat"

    def test_empty_input(self) -> None:
        assert longest_word("") is None

    def test_only_whitespace(self) -> None:
        assert longest_word("   ") is None

    def test_single_token(self) -> None:
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
    def test_is_palindrome_param(self, text: str, expected: bool) -> None:
        assert is_palindrome(text) == expected

    def test_punctuation_ignored(self) -> None:
        assert is_palindrome("Madam, I'm Adam.") is True

    def test_repeated_char(self) -> None:
        assert is_palindrome("aaaa") is True