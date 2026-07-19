from __future__ import annotations

VOWELS: frozenset[str] = frozenset({"a", "e", "i", "o", "u"})


def count_vowels(text: str) -> dict[str, int]:
    """Count each vowel (a, e, i, o, u) in *text*, case-insensitive."""
    result: dict[str, int] = {vowel: 0 for vowel in sorted(VOWELS)}
    for character in text.casefold():
        if character in result:
            result[character] += 1
    return result


def longest_word(text: str) -> str | None:
    """Return the first longest whitespace-delimited word, or None if empty."""
    words = text.split()
    if not words:
        return None
    return max(words, key=len)


def is_palindrome(text: str) -> bool:
    """Return True if *text* reads the same forwards and backwards.

    Case, whitespace and punctuation are ignored; the empty string is a
    palindrome.
    """
    cleaned = "".join(character for character in text.casefold() if character.isalnum())
    return cleaned == cleaned[::-1]
