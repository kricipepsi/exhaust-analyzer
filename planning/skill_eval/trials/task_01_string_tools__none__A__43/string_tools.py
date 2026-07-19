"""String analysis utilities."""

from __future__ import annotations

VOWEL_SET = frozenset("aeiou")


def count_vowels(text: str) -> dict[str, int]:
    """Return a dict with counts for each vowel (a, e, i, o, u).

    Case-insensitive. Non-vowels are ignored.

    Args:
        text: Input string.

    Returns:
        Dict mapping lowercase vowel to its count.
    """
    counts: dict[str, int] = {v: 0 for v in "aeiou"}
    for ch in text.casefold():
        if ch in counts:
            counts[ch] += 1
    return counts


def longest_word(text: str) -> str | None:
    """Return the longest whitespace-delimited word in text.

    Ties go to the first occurrence. Returns None for empty or blank input.

    Args:
        text: Input string.

    Returns:
        The longest word, or None if none found.
    """
    parts = text.split()
    if not parts:
        return None
    return max(parts, key=len)


def is_palindrome(text: str) -> bool:
    """Test whether text is a palindrome, ignoring case, spaces, and punctuation.

    Args:
        text: Input string.

    Returns:
        True if palindrome, False otherwise.
    """
    cleaned = [c.casefold() for c in text if c.isalnum()]
    return cleaned == cleaned[::-1]