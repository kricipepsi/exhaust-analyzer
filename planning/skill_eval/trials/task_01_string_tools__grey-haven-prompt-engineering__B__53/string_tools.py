"""String analysis helpers."""

from __future__ import annotations

_VOWELS = frozenset("aeiou")


def count_vowels(text: str) -> dict[str, int]:
    """Return a dict mapping each vowel (a, e, i, o, u) to its count.

    Case-insensitive. Non-vowel characters are ignored.

    Args:
        text: Input string to analyze.

    Returns:
        Dict with vowel counts.
    """
    counts: dict[str, int] = {v: 0 for v in "aeiou"}
    for char in text.casefold():
        if char in counts:
            counts[char] += 1
    return counts


def longest_word(text: str) -> str | None:
    """Return the longest whitespace-delimited word in text.

    First occurrence wins on ties. Returns None for empty/blank input.

    Args:
        text: Input string.

    Returns:
        Longest word, or None.
    """
    words = text.split()
    if not words:
        return None
    return max(words, key=len)


def is_palindrome(text: str) -> bool:
    """Test if text reads the same forwards and backwards.

    Ignores case, spaces, and punctuation. Empty string is palindrome.

    Args:
        text: Input string to test.

    Returns:
        True if palindrome.
    """
    filtered = [c.casefold() for c in text if c.isalnum()]
    return filtered == filtered[::-1]