from __future__ import annotations

from collections.abc import Callable
from functools import lru_cache

VOWELS: frozenset[str] = frozenset({"a", "e", "i", "o", "u"})


def count_vowels(text: str) -> dict[str, int]:
    """Return per-vowel frequency (case-insensitive)."""
    return _tally(text.casefold(), _is_vowel)


def longest_word(text: str) -> str | None:
    """Return the first longest whitespace-delimited word, or None."""
    words = text.split()
    return max(words, key=len) if words else None


@lru_cache(maxsize=256)
def is_palindrome(text: str) -> bool:
    """Return True when *text* is a palindrome (case/punctuation-insensitive)."""
    cleaned = "".join(filter(str.isalnum, text.casefold()))
    return cleaned == cleaned[::-1]


# ---- internal ----

def _tally(text: str, predicate: Callable[[str], bool]) -> dict[str, int]:
    """Count occurrences of characters in *text* that satisfy *predicate*."""
    counts: dict[str, int] = {}
    for ch in text:
        if predicate(ch):
            counts[ch] = counts.get(ch, 0) + 1
    # Ensure all vowels present even if count is zero
    return {v: counts.get(v, 0) for v in sorted(VOWELS)}


def _is_vowel(ch: str) -> bool:
    return ch in VOWELS
