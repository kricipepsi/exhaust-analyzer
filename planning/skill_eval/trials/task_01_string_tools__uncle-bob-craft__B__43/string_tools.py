from __future__ import annotations

_VOWEL_SET = frozenset({"a", "e", "i", "o", "u"})


def count_vowels(text: str) -> dict[str, int]:
    """Return per-vowel frequency map (case-insensitive)."""
    counts = _empty_vowel_map()
    for character in text.casefold():
        if _is_vowel(character):
            counts[character] += 1
    return counts


def longest_word(text: str) -> str | None:
    """Return the first word with the greatest character count."""
    words = _extract_words(text)
    if not words:
        return None
    return _longest_by_length(words)


def is_palindrome(text: str) -> bool:
    """Return True when *text* equals itself reversed (ignoring case/punctuation)."""
    stripped = _strip_to_alphanumeric(text)
    return stripped == _reverse(stripped)


# ---- private helpers ----

def _empty_vowel_map() -> dict[str, int]:
    return {v: 0 for v in sorted(_VOWEL_SET)}


def _is_vowel(character: str) -> bool:
    return character in _VOWEL_SET


def _extract_words(text: str) -> list[str]:
    return text.split()


def _longest_by_length(words: list[str]) -> str:
    return max(words, key=len)


def _strip_to_alphanumeric(text: str) -> str:
    return "".join(ch for ch in text.casefold() if ch.isalnum())


def _reverse(text: str) -> str:
    return text[::-1]
