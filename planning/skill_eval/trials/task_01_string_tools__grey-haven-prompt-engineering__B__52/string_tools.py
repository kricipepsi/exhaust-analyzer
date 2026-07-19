"""String tools module - text analysis functions."""

from __future__ import annotations


def count_vowels(text: str) -> dict[str, int]:
    """Count each vowel (a, e, i, o, u) in text, case-insensitive.

    Args:
        text: The string to count vowels in.

    Returns:
        Dict mapping each vowel to its occurrence count. Non-vowels are skipped.
    """
    result: dict[str, int] = {v: 0 for v in "aeiou"}
    for ch in text.lower():
        if ch in result:
            result[ch] += 1
    return result


def longest_word(text: str) -> str | None:
    """Find the longest whitespace-delimited word in text.

    Returns the first word when multiple words share the maximum length.
    Returns None for empty or blank input.

    Args:
        text: The string to search.

    Returns:
        The longest word, or None if no words exist.
    """
    words = text.split()
    if not words:
        return None
    return max(words, key=len)


def is_palindrome(text: str) -> bool:
    """Check if text is a palindrome.

    Case, spaces, and punctuation are ignored. Empty string is a palindrome.

    Args:
        text: The string to test.

    Returns:
        True if the text is a palindrome.
    """
    cleaned = [c.lower() for c in text if c.isalnum()]
    return cleaned == cleaned[::-1]