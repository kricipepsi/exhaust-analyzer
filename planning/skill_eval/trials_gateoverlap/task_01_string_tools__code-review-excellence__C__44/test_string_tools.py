from __future__ import annotations

import pytest
from string_tools import count_vowels, is_palindrome, longest_word


def test_count_vowels_case_insensitive() -> None:
    assert count_vowels("AaEe") == {"a": 2, "e": 2, "i": 0, "o": 0, "u": 0}


@pytest.mark.parametrize("text,expected", [("cat dog bat", "cat"), ("", None)])
def test_longest_word_edge_cases(text: str, expected: str | None) -> None:
    assert longest_word(text) == expected


@pytest.mark.parametrize(
    "text,expected",
    [("racecar", True), ("No lemon, no melon", True), ("hello", False), ("", True)],
)
def test_is_palindrome(text: str, expected: bool) -> None:
    assert is_palindrome(text) == expected
