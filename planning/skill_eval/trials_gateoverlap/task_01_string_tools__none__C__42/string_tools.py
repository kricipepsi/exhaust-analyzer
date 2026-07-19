def count_vowels(text):
    counts = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
    for ch in text.lower():
        if ch in counts:
            counts[ch] += 1
    return counts


def longest_word(text):
    words = text.split()
    if not words:
        return None
    best = words[0]
    for w in words:
        if len(w) >= len(best):   # BUG: ties resolve to the LAST word
            best = w
    return best


def is_palindrome(text):
    t = text.lower().replace(" ", "")   # BUG: only strips spaces, not punctuation
    return t == t[::-1]
