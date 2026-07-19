from __future__ import annotations

import pytest
from string_tools import count_vowels, is_palindrome, longest_word


def test_count_vowels_returns_all_five_keys_regression() -> None:
    """GUARD: result must always carry all five vowel keys, even on no match."""
    result = count_vowels("xyz")
    assert set(result) == {"a", "e", "i", "o", "u"}


def test_count_vowels_case_fold_boundary_regression() -> None:
    """GUARD: uppercase vowels must be counted (casefold path)."""
    assert count_vowels("AEIOU") == {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1}


def test_longest_word_empty_returns_none_not_empty_string_regression() -> None:
    """GUARD: empty input must return None, not '' (the None branch)."""
    assert longest_word("") is None
    assert longest_word("   ") is None


def test_longest_word_tie_keeps_first_regression() -> None:
    """GUARD: ties resolve to the first occurrence, not the last."""
    assert longest_word("cat dog bat") == "cat"


def test_is_palindrome_empty_is_true_boundary_regression() -> None:
    """GUARD: the empty string is a palindrome (boundary input)."""
    assert is_palindrome("") is True


def test_is_palindrome_non_palindrome_is_false_regression() -> None:
    """GUARD: a clear non-palindrome must be False (no always-True drift)."""
    assert is_palindrome("hello") is False
    assert is_palindrome("ab") is False


@pytest.mark.parametrize("text", ["racecar", "A man a plan a canal Panama"])
def test_is_palindrome_known_true_cases_regression(text: str) -> None:
    """GUARD: known palindromes stay True across punctuation/space stripping."""
    assert is_palindrome(text) is True
