# Python Performance Reference

## The Cardinal Rule

**Profile first. Optimise second. Never guess.**

```
Get it right → Test it's right → Profile if slow → Optimise → Repeat from step 2
```

Premature optimisation is the root of most unreadable Python. Profile before touching anything.

---

## Profiling Tools

### cProfile (built-in, start here)

```bash
# Profile a script
python -m cProfile -o profile.pstats myscript.py arg1 arg2

# View results
python -c "
import pstats
p = pstats.Stats('profile.pstats')
p.sort_stats('cumulative')
p.print_stats(20)
"
```

Key columns: `cumtime` (total time including callees), `tottime` (own time only), `ncalls`.

### line_profiler (line-by-line timing)

```bash
pip install line_profiler
```

```python
# Decorate the function you want to profile
@profile  # added at runtime by kernprof
def slow_function(data):
    ...
```

```bash
kernprof -l -v myscript.py
```

Shows microseconds per line — great for finding the exact slow line.

### memory_profiler (memory by line)

```bash
pip install memory_profiler
```

```python
from memory_profiler import profile

@profile
def memory_hungry():
    big_list = [x**2 for x in range(1_000_000)]  # allocated here
    ...
```

```bash
python -m memory_profiler myscript.py
```

### Py-Spy (sampling profiler — zero overhead, works on running processes)

```bash
pip install py-spy

# Top-like view
py-spy top --pid <pid>

# Flame graph (open in browser)
py-spy record -o profile.svg --pid <pid>
```

Best for production profiling without stopping the process.

### timeit (micro-benchmarks)

```python
import timeit

# Quick one-liner
t = timeit.timeit("'-'.join(str(n) for n in range(100))", number=100_000)
print(f"{t:.3f}s for 100k iterations")

# Compare two approaches
results = timeit.repeat(
    stmt="[x**2 for x in range(1000)]",
    repeat=5,
    number=1000
)
print(f"min={min(results):.3f}s")
```

---

## Common Bottlenecks and Fixes

### 1. Algorithmic Complexity (biggest wins here)

Before any micro-optimisation, check the algorithm:

| Bad | Better | Why |
|-----|--------|-----|
| `if item in my_list` (O(n)) | `if item in my_set` (O(1)) | Set lookup is hash-based |
| Nested loop O(n²) | Sort + merge O(n log n) | |
| Repeated DB queries in loop | Bulk fetch | N+1 problem |
| Re-reading file in loop | Load once, process | I/O is slow |

### 2. String Concatenation

```python
# BAD — O(n²): creates new string object each iteration
result = ""
for item in items:
    result += str(item) + ", "

# GOOD — O(n)
result = ", ".join(str(item) for item in items)
```

### 3. Attribute / Method Lookup in Hot Loops

```python
import math

# Slow — Python looks up math.sqrt on every iteration
for i in range(100_000):
    results.append(math.sqrt(i))

# Fast — cache the reference
sqrt = math.sqrt
append = results.append
for i in range(100_000):
    append(sqrt(i))
```

### 4. Global vs Local Variable Lookup

Local variable access is ~2× faster than global. In tight loops:

```python
def process(items):
    # Localise frequently-used built-ins
    _len = len
    _str = str
    for item in items:
        if _len(item) > 10:
            yield _str(item)
```

### 5. List vs Generator

```python
# List — allocates everything upfront
squares = [x**2 for x in range(1_000_000)]  # ~8MB in memory

# Generator — allocates almost nothing, lazy
squares = (x**2 for x in range(1_000_000))  # ~128 bytes

# Use generators when:
# - You only iterate once
# - The sequence is large
# - You're chaining operations (pipeline)
total = sum(x**2 for x in range(1_000_000))  # never creates the list
```

### 6. Import Overhead

```python
# DON'T import inside frequently-called functions
def process():
    import json  # This adds overhead each call
    ...

# DO import at module level
import json

def process():
    json.loads(data)
```

Exception: lazy imports for rarely-used heavy modules at the top of the file:
```python
_numpy = None

def get_numpy():
    global _numpy
    if _numpy is None:
        import numpy as _numpy
    return _numpy
```

### 7. Choosing Data Structures

| Task | Use | Why |
|------|-----|-----|
| Ordered sequence, index access | `list` | O(1) indexing |
| Membership test | `set` or `frozenset` | O(1) vs O(n) |
| Key-value store | `dict` | O(1) get/set |
| Queue (add/remove from both ends) | `collections.deque` | O(1) both ends vs O(n) list.insert(0) |
| Sorted data | `bisect` + `list` | Binary search O(log n) |
| Priority queue | `heapq` | O(log n) push/pop |
| Count occurrences | `collections.Counter` | Optimised C impl |

### 8. Caching Expensive Results

```python
from functools import lru_cache, cache

# Unlimited cache (Python 3.9+)
@cache
def compute_expensive(n: int) -> float:
    ...

# Bounded cache (evicts oldest when full)
@lru_cache(maxsize=256)
def lookup(key: str) -> dict:
    ...

# Manual cache for non-hashable args
_cache: dict = {}
def get_data(params: dict) -> list:
    key = frozenset(params.items())
    if key not in _cache:
        _cache[key] = _fetch(params)
    return _cache[key]
```

### 9. __slots__ for Many Instances

```python
# Without __slots__: each instance has a __dict__ (~100-200 bytes overhead)
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# With __slots__: no __dict__, direct attribute storage (~40-60% less memory)
@dataclass(slots=True)  # Python 3.10+
class Point:
    x: float
    y: float

# When 100k+ instances exist, this matters
```

### 10. Avoid Repeated Computation in Loops

```python
# Bad — len() called on every iteration
for i in range(len(items)):
    if i < len(items) - 1:  # called again!
        ...

# Good — compute once
n = len(items)
for i in range(n):
    if i < n - 1:
        ...
```

---

## Concurrency Patterns

### I/O-Bound: asyncio

```python
import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.json()

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*[fetch(session, u) for u in urls])
```

### I/O-Bound (simpler): ThreadPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def download(url):
    ...

urls = [...]
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(download, url): url for url in urls}
    for future in as_completed(futures):
        url = futures[future]
        try:
            result = future.result()
        except Exception as exc:
            logger.error("Failed %s: %s", url, exc)
```

### CPU-Bound: ProcessPoolExecutor

```python
from concurrent.futures import ProcessPoolExecutor

def cpu_heavy(data):
    # actual computation
    ...

with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(cpu_heavy, chunks))
```

Note: Python's GIL means threads don't help for CPU-bound work. Use processes.

---

## NumPy for Numerical Work

If processing arrays of numbers, numpy is orders of magnitude faster than Python loops:

```python
import numpy as np

# Python loop — slow
squares = [x**2 for x in range(1_000_000)]

# NumPy — C-speed
arr = np.arange(1_000_000)
squares = arr ** 2  # vectorised, ~100× faster

# Vectorised operations
mean = arr.mean()
std = arr.std()
filtered = arr[arr > 0]  # boolean indexing
```

Don't use `numpy.mean()` for small Python lists though — `sum()/len()` is faster due to no import overhead.
