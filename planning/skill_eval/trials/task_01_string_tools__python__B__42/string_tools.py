from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

VOWELS: frozenset[str] = frozenset({"a", "e", "i", "o", "u"})
EMPTY_COUNTS: dict[str, int] = {v: 0 for v in sorted(VOWELS)}


def count_vowels(text: str) -> dict[str, int]:
    """Count each vowel (a, e, i, o, u) in *text*, case-insensitive.

    Returns a dict mapping each vowel to its count. Non-vowel characters
    are ignored.
    """
    result: dict[str, int] = {v: 0 for v in sorted(VOWELS)}
    for ch in text.casefold():
        if ch in result:
            result[ch] += 1
    return result


def longest_word(text: str) -> str | None:
    """Return the longest whitespace-delimited word in *text*.

    On ties, returns the first occurrence.  Returns ``None`` when *text*
    is empty or contains only whitespace.
    """
    words = text.split()
    if not words:
        return None
    return max(words, key=len)


def is_palindrome(text: str) -> bool:
    """Return ``True`` if *text* reads the same forwards and backwards.

    Case, whitespace and punctuation are ignored.  An empty string is
    considered a palindrome.
    """
    cleaned = "".join(ch for ch in text.casefold() if ch.isalnum())
    return cleaned == cleaned[::-1]
