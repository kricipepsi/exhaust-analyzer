"""Text analysis helpers - string operations module."""

from __future__ import annotations


def count_vowels(text: str) -> dict[str, int]:
    """Count each vowel (a, e, i, o, u) in text, case-insensitive.

    Args:
        text: Input text to scan.

    Returns:
        Dict with vowel keys and integer counts. Non-vowels excluded.
    """
    vowels = "aeiou"
    tally: dict[str, int] = dict.fromkeys(vowels, 0)
    for letter in text.lower():
        if letter in tally:
            tally[letter] += 1
    return tally


def longest_word(text: str) -> str | None:
    """Return the longest whitespace-separated word.

    First occurrence wins ties. Returns None if text is empty or all whitespace.

    Args:
        text: Input text.

    Returns:
        Longest word string, or None.
    """
    tokens = text.split()
    if not tokens:
        return None
    longest_so_far = tokens[0]
    for token in tokens[1:]:
        if len(token) > len(longest_so_far):
            longest_so_far = token
    return longest_so_far


def is_palindrome(text: str) -> bool:
    """Return True if text is a palindrome.

    Ignores case, whitespace, and punctuation. Empty string is a palindrome.

    Args:
        text: Input text.

    Returns:
        True if palindrome, False otherwise.
    """
    stripped = [c.lower() for c in text if c.isalnum()]
    return stripped == list(reversed(stripped))