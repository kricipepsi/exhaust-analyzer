# Python Idioms & Patterns Reference

## Built-in Functions — Use Them

Python's built-ins are implemented in C. Prefer them over manual equivalents.

```python
# sum / min / max / sorted / any / all
total = sum(prices)
cheapest = min(products, key=lambda p: p.price)
ordered = sorted(data, key=lambda x: x["age"], reverse=True)

# any / all — short-circuit evaluation
has_errors = any(r.failed for r in results)
all_valid = all(isinstance(x, int) for x in items)

# map / filter — use sparingly; comprehensions usually clearer
upper_names = list(map(str.upper, names))  # OK for simple method calls
filtered = [x for x in items if x > 0]    # prefer comprehension with condition
```

## Iteration Patterns

```python
# enumerate — index + value
for i, item in enumerate(items, start=1):  # start=1 for 1-based index
    print(f"{i}. {item}")

# zip — parallel iteration (stops at shortest)
for key, value in zip(keys, values):
    ...

# zip_longest — parallel with fill value
from itertools import zip_longest
for a, b in zip_longest(list1, list2, fillvalue=None):
    ...

# zip to create dict
mapping = dict(zip(keys, values))

# Unpacking
first, *middle, last = sequence
a, b = b, a  # swap

# next() with default — find first match
found = next((x for x in items if x.active), None)

# Walrus in loops
while chunk := file.read(8192):
    process(chunk)

# itertools for complex iteration
from itertools import chain, islice, groupby, product, combinations

# chain — flatten iterables
all_items = list(chain(list1, list2, list3))

# islice — lazy slice of iterator
first_100 = list(islice(big_generator, 100))

# groupby — group consecutive items (sort first!)
from itertools import groupby
for key, group in groupby(sorted_data, key=lambda x: x.category):
    items = list(group)
```

## Comprehensions

```python
# List
squares = [x**2 for x in range(10)]

# Dict
freq = {word: words.count(word) for word in set(words)}

# Set
unique_lengths = {len(word) for word in words}

# Generator (lazy — use when you don't need a list)
total = sum(x**2 for x in range(10_000))

# Nested (flatten)
flat = [item for row in matrix for item in row]

# With condition
evens = [x for x in nums if x % 2 == 0]
categorized = ["even" if x % 2 == 0 else "odd" for x in nums]

# AVOID: complex nested comprehensions — use a regular loop if it takes >1 read
```

## Functional Tools

```python
from functools import partial, reduce, singledispatch

# partial — fix some arguments
double = partial(pow, exp=2)

# reduce — fold (use sparingly; often a loop is clearer)
from functools import reduce
product = reduce(lambda x, y: x * y, nums)

# singledispatch — type-based dispatch (replaces if/elif type checks)
@singledispatch
def normalize(value):
    raise TypeError(f"Unsupported type: {type(value)}")

@normalize.register
def _(value: str) -> str:
    return value.strip().lower()

@normalize.register
def _(value: int) -> str:
    return str(value)

@normalize.register
def _(value: list) -> list:
    return [normalize(v) for v in value]
```

## Decorators

```python
import functools
import time

# Basic decorator
def timer(func):
    @functools.wraps(func)  # preserve __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.3f}s")
        return result
    return wrapper

# Decorator with arguments
def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (attempt + 1))
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def fetch_data(url: str) -> dict:
    ...
```

## Context Managers

```python
from contextlib import contextmanager, suppress

# Custom context manager
@contextmanager
def timed_section(name: str):
    """Context manager that logs how long a section takes."""
    start = time.perf_counter()
    try:
        yield
    finally:
        duration = time.perf_counter() - start
        logger.info("%s completed in %.3fs", name, duration)

with timed_section("data_sync"):
    sync_remote_data()

# Suppress specific errors
with suppress(FileNotFoundError):
    cache_path.unlink()

# Class-based (for more complex state)
class ManagedResource:
    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._disconnect()
        return False  # don't suppress exceptions
```

## Collections Toolbox

```python
from collections import Counter, defaultdict, OrderedDict, deque, namedtuple
from collections import ChainMap

# Counter
word_freq = Counter(text.split())
top_5 = word_freq.most_common(5)
word_freq["unknown"]  # returns 0, not KeyError

# defaultdict
graph = defaultdict(set)
graph["A"].add("B")  # no need to check if "A" exists

# deque — O(1) from both ends; use as queue
queue = deque(maxlen=100)  # auto-drops oldest when full
queue.appendleft(item)
queue.pop()

# namedtuple — lightweight, immutable records
Point = namedtuple("Point", ["x", "y"])
# or with typing:
from typing import NamedTuple
class Point(NamedTuple):
    x: float
    y: float
    label: str = ""

# ChainMap — layered dict lookup
from collections import ChainMap
combined = ChainMap(user_overrides, project_defaults, global_defaults)
```

## String Operations

```python
# f-strings (prefer over format/%)
name, count = "Alice", 42
msg = f"Hello {name}, you have {count} messages"
debug = f"{count=}"            # "count=42"
price = f"{amount:.2f}"        # formatted float
padded = f"{name:>20}"         # right-align in 20 chars

# Join (never += in a loop)
csv_line = ",".join(str(x) for x in row)

# Split / strip / replace
words = text.strip().split()
cleaned = " ".join(text.split())  # collapse whitespace

# Check prefix/suffix (Python 3.9+)
if path.endswith((".jpg", ".png", ".gif")):
    ...

# textwrap for long strings
import textwrap
wrapped = textwrap.fill(long_text, width=80)
```

## Numbers and Dates

```python
# Readable large numbers
population = 1_000_000
pi_approx = 3.141_592_653

# Decimal for money (never float!)
from decimal import Decimal
price = Decimal("19.99")
tax = price * Decimal("0.08")

# datetime
from datetime import datetime, timezone, timedelta
now = datetime.now(tz=timezone.utc)  # always UTC
tomorrow = now + timedelta(days=1)
formatted = now.strftime("%Y-%m-%dT%H:%M:%SZ")
parsed = datetime.fromisoformat("2024-01-15T10:30:00+00:00")
```

## File Operations

```python
from pathlib import Path

# Prefer pathlib over os.path
base = Path("data")
output = base / "results" / "final.csv"
output.parent.mkdir(parents=True, exist_ok=True)

# Read
text = output.read_text(encoding="utf-8")
lines = output.read_text().splitlines()

# Write
output.write_text(content, encoding="utf-8")

# Iterate files
for path in base.rglob("*.csv"):
    process(path)

# Safe temp files
import tempfile
with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
    temp_path = Path(f.name)
    f.write(data)
```
