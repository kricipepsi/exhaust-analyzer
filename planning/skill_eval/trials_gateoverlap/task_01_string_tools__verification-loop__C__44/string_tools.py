from __future__ import annotations


def count_vowels(text: str) -> dict[str, int]:
    counts = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
    for ch in text.lower():
        if ch in counts:
            counts[ch] += 1
    return counts


def longest_word(text: str) -> str | None:
    words = text.split()
    if not words:
        return None
    longest = ""
    for w in words:
        if len(w) >= len(longest):   # BUG: ties resolve to the LAST word
            longest = w
    return longest


def is_palindrome(text: str) -> bool:
    stripped = text.lower().replace(" ", "")   # BUG: punctuation not stripped
    return stripped == stripped[::-1]
