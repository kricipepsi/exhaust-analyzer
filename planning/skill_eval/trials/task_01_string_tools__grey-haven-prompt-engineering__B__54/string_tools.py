"""Text utilities for string processing."""

from __future__ import annotations

VOWEL_LETTERS = frozenset("aeiou")


def count_vowels(text: str) -> dict[str, int]:
    """Count occurrences of each vowel (a, e, i, o, u) in the given text.

    The count is case-insensitive. Characters that are not vowels are ignored.

    Args:
        text: The text to examine.

    Returns:
        A dictionary mapping each vowel to the number of times it appears.
    """
    counters: dict[str, int] = dict.fromkeys("aeiou", 0)
    for c in text.lower():
        if c in counters:
            counters[c] += 1
    return counters


def longest_word(text: str) -> str | None:
    """Identify the longest word in text, delimited by whitespace.

    When multiple words have the same maximum length, the first one is returned.
    Returns None if the text is empty or whitespace-only.

    Args:
        text: The text to search.

    Returns:
        The longest word, or None.
    """
    tokens = text.split()
    if not tokens:
        return None
    longest = tokens[0]
    for w in tokens[1:]:
        if len(w) > len(longest):
            longest = w
    return longest


def is_palindrome(text: str) -> bool:
    """Determine whether text reads identically forwards and backwards.

    Case, whitespace, and punctuation are all ignored in the comparison.
    An empty string is considered a palindrome.

    Args:
        text: The text to test.

    Returns:
        True if the text is palindromic.
    """
    alpha_only = [c.lower() for c in text if c.isalnum()]
    return alpha_only == alpha_only[::-1]