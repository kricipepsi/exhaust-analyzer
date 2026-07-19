# Task: String Tools Module

**Difficulty:** Easy · **Type:** Synthetic · **Primary axes:** first-pass quality, rubric (readability/naming/structure)

## Prompt

Write a Python module `string_tools.py` with three functions:

1. `count_vowels(text: str) -> dict[str, int]` — returns a dict mapping each vowel
   (a, e, i, o, u, case-insensitive) to its count in `text`. Non-vowel characters
   are ignored.

2. `longest_word(text: str) -> str | None` — returns the longest word in `text`
   (words are separated by whitespace). If multiple words tie for longest, return
   the first one. Returns `None` if `text` is empty or contains no words.

3. `is_palindrome(text: str) -> bool` — returns True if `text` reads the same
   forwards and backwards, ignoring case, spaces, and punctuation. Empty string
   is a palindrome.

Also write `test_string_tools.py` with pytest tests covering:
- Normal cases for each function
- Edge cases (empty input, single character, all same character)
- At least one parametrized test

## Requirements

- Python 3.10+ with type hints on all function signatures
- Docstrings on all public functions
- No mutable default arguments
- Use pathlib if any file I/O is needed
- Tests pass with `pytest test_string_tools.py -v`

## Output

Write `string_tools.py` and `test_string_tools.py` in the working directory.
