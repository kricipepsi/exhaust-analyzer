"""Test suite for text utilities."""

from __future__ import annotations

import pytest

from string_tools import count_vowels, is_palindrome, longest_word


class TestCountVowels:
    def test_basic_case(self) -> None:
        got = count_vowels("hello world")
        want = {"a": 0, "e": 1, "i": 0, "o": 2, "u": 0}
        assert got == want

    def test_empty_input(self) -> None:
        got = count_vowels("")
        want = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
        assert got == want

    def test_all_vowels_once(self) -> None:
        assert count_vowels("aeiou") == {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1}

    def test_no_vowels_present(self) -> None:
        got = count_vowels("rhythm")
        want = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
        assert got == want

    def test_case_is_ignored(self) -> None:
        got = count_vowels("AaEeIiOoUu")
        want = {"a": 2, "e": 2, "i": 2, "o": 2, "u": 2}
        assert got == want


class TestLongestWord:
    def test_basic(self) -> None:
        assert longest_word("the quick brown fox") == "quick"

    def test_first_wins_on_tie(self) -> None:
        assert longest_word("cat dog bat") == "cat"

    def test_empty_string(self) -> None:
        assert longest_word("") is None

    def test_whitespace_string(self) -> None:
        assert longest_word("   ") is None

    def test_one_token(self) -> None:
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
    def test_palindrome_parametrized(self, text: str, expected: bool) -> None:
        assert is_palindrome(text) == expected

    def test_punctuation_and_spacing_ignored(self) -> None:
        assert is_palindrome("Madam, I'm Adam.") is True

    def test_single_char_repeated(self) -> None:
        assert is_palindrome("aaaa") is True