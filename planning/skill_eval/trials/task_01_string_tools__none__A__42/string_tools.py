"""String utility functions for text analysis."""

from __future__ import annotations

VOWELS = frozenset("aeiou")


def count_vowels(text: str) -> dict[str, int]:
    """Count occurrences of each vowel (a, e, i, o, u) in text, case-insensitive.

    Args:
        text: The input string to analyze.

    Returns:
        A dict mapping each vowel character to its count. Non-vowel characters are ignored.
    """
    result: dict[str, int] = {v: 0 for v in "aeiou"}
    for char in text.lower():
        if char in result:
            result[char] += 1
    return result


def longest_word(text: str) -> str | None:
    """Find the longest word in text by whitespace separation.

    If multiple words tie for longest, returns the first one encountered.
    Returns None if text is empty or contains no words.

    Args:
        text: The input string to analyze.

    Returns:
        The longest word, or None.
    """
    words = text.split()
    if not words:
        return None
    return max(words, key=len)


def is_palindrome(text: str) -> bool:
    """Check if text reads the same forwards and backwards.

    Ignores case, spaces, and punctuation. Empty string is a palindrome.

    Args:
        text: The input string to check.

    Returns:
        True if text is a palindrome.
    """
    filtered = [c.lower() for c in text if c.isalnum()]
    return filtered == filtered[::-1]