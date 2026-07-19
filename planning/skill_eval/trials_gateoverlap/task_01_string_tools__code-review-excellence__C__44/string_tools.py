from __future__ import annotations

_VOWELS = ("a", "e", "i", "o", "u")


def count_vowels(text: str) -> dict[str, int]:
    """Return a count of each vowel (a, e, i, o, u) in *text*, case-insensitive."""
    counts = {vowel: 0 for vowel in _VOWELS}
    for character in text.lower():
        if character in counts:
            counts[character] += 1
    return counts


def longest_word(text: str) -> str | None:
    """Return the first longest whitespace-delimited word, or None if empty.

    Ties resolve to the first occurrence (reviewed edge case).
    """
    words = text.split()
    if not words:
        return None
    longest = words[0]
    for word in words[1:]:
        if len(word) > len(longest):   # strict > keeps the FIRST of equal-length
            longest = word
    return longest


def is_palindrome(text: str) -> bool:
    """Return True if *text* is a palindrome ignoring case, spaces, punctuation.

    The empty string is a palindrome (reviewed boundary case).
    """
    cleaned = "".join(character for character in text.lower() if character.isalnum())
    return cleaned == cleaned[::-1]
