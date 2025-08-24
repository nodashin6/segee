# Usage Guide

## Basic Usage

### Specialized Classes (Recommended)

Segee provides three convenience classes for common operations:

#### SumSegmentTree
```python
from segee import SumSegmentTree

# Create a sum segment tree
tree = SumSegmentTree(5)

# Set values
tree.set(0, 10)
tree.set(1, 20)
tree.set(2, 30)

# Range sum queries
print(tree.sum(0, 2))    # 30 (sum of indices 0-1)
print(tree.sum(0, 3))    # 60 (sum of indices 0-2)
print(tree.total())      # 60 (sum of all elements)

# Pythonic access
tree[1] = 25
print(tree[0:3])         # [10, 25, 30]
```

#### MinSegmentTree
```python
from segee import MinSegmentTree

# Create a min segment tree
tree = MinSegmentTree(5)

# Set values
tree.set(0, 10)
tree.set(1, 5)
tree.set(2, 20)

# Range minimum queries
print(tree.minimum(0, 2))   # 5 (min of indices 0-1)
print(tree.minimum(0, 3))   # 5 (min of indices 0-2)
print(tree.global_min())    # 5 (minimum of all elements)
```

#### MaxSegmentTree
```python
from segee import MaxSegmentTree

# Create a max segment tree
tree = MaxSegmentTree(5)

# Set values
tree.set(0, 10)
tree.set(1, 25)
tree.set(2, 15)

# Range maximum queries
print(tree.maximum(0, 2))   # 25 (max of indices 0-1)
print(tree.maximum(0, 3))   # 25 (max of indices 0-2)
print(tree.global_max())    # 25 (maximum of all elements)
```

### Generic SegmentTree

For custom operations, use the generic `SegmentTree` class:

```python
import operator
import math
from segee import SegmentTree

# Sum segment tree
sum_tree = SegmentTree(size=5, identity=0, operation=operator.add)

# Min segment tree
min_tree = SegmentTree(size=5, identity=float('inf'), operation=min)

# Max segment tree  
max_tree = SegmentTree(size=5, identity=float('-inf'), operation=max)

# GCD segment tree
gcd_tree = SegmentTree(size=5, identity=0, operation=math.gcd)

# String concatenation
concat_tree = SegmentTree(size=3, identity="", operation=operator.add)
```

## Advanced Features

### Binary Search Operations

#### max_right
Find the maximum right boundary where a predicate holds:

```python
tree = SumSegmentTree(5)
tree[0:5] = [1, 2, 3, 4, 5]

# Find max right where sum <= 6
result = tree.max_right(0, lambda x: x <= 6)
print(result)  # 3 (sum([1, 2, 3]) = 6 <= 6)
```

#### min_left  
Find the minimum left boundary where a predicate holds:

```python
tree = SumSegmentTree(5)
tree[0:5] = [1, 2, 3, 4, 5]

# Find min left where sum >= 7
result = tree.min_left(5, lambda x: x >= 7)
print(result)  # 2 (sum([3, 4, 5]) = 12 >= 7)
```

### Sequence Protocol

Segee segment trees implement Python's sequence protocol:

```python
tree = SumSegmentTree(5)

# Length
print(len(tree))         # 5

# Item access
tree[0] = 10
print(tree[0])           # 10

# Slicing
tree[1:4] = [20, 30, 40]
print(tree[1:4])         # [20, 30, 40]

# Membership
print(10 in tree)        # True

# Iteration
for value in tree:
    print(value)

# Equality
other_tree = SumSegmentTree(5)
other_tree[0:5] = [10, 20, 30, 40, 0]
print(tree == other_tree)  # True
```

### Negative Indexing

All segment trees support negative indexing:

```python
tree = SumSegmentTree(5)
tree[-1] = 100           # Set last element
print(tree.get(-1))      # 100
print(tree.get(4))       # 100 (same element)
```

## Error Handling

Segee provides comprehensive error handling with custom exception types:

```python
from segee import SegmentTreeIndexError, SegmentTreeRangeError

try:
    tree = SumSegmentTree(5)
    tree.get(10)  # Index out of bounds
except SegmentTreeIndexError as e:
    print(f"Index {e.index} is invalid for tree of size {e.size}")

try:
    tree.sum(-1, 3)  # Invalid range
except SegmentTreeRangeError as e:
    print(f"Range [{e.left}, {e.right}) is invalid for tree of size {e.size}")
```

## Performance Considerations

### When to Use Segment Trees

Segment trees are optimal when:
- **Large datasets** (n > 1000)
- **Many queries** (q > 1000) 
- **Mixed updates and queries**

For small datasets (n < 1000, q < 1000), naive O(n) approaches may be faster due to constant factor overhead.

### Memory Usage

- **Space complexity**: O(n)
- **Typical memory**: ~4x the input array size
- **Cache friendly**: Tree structure optimizes memory access patterns

### Benchmarking Your Use Case

```python
import time
from segee import SumSegmentTree

# Benchmark segment tree
tree = SumSegmentTree(100000)
start = time.time()
for i in range(10000):
    tree.sum(i, i + 1000)
segment_time = time.time() - start

# Compare with naive approach
arr = [0] * 100000
start = time.time()
for i in range(10000):
    sum(arr[i:i + 1000])
naive_time = time.time() - start

print(f"Segment tree: {segment_time:.4f}s")
print(f"Naive approach: {naive_time:.4f}s")
```

## Common Patterns

### Range Sum with Updates
```python
tree = SumSegmentTree(n)
# Process updates and queries efficiently
for query_type, *args in queries:
    if query_type == 'update':
        tree.set(args[0], args[1])
    else:  # query
        result = tree.sum(args[0], args[1])
```

### Range Minimum with Binary Search
```python
tree = MinSegmentTree(n)
# Find first position where minimum >= threshold
pos = tree.max_right(0, lambda x: x >= threshold)
```

### Multiple Segment Trees
```python
# Track both sum and minimum simultaneously
sum_tree = SumSegmentTree(n)
min_tree = MinSegmentTree(n)

for i, value in enumerate(data):
    sum_tree.set(i, value)
    min_tree.set(i, value)
```

## Type Hints

Segee provides complete type hints for all operations:

```python
from typing import Protocol
from segee import SegmentTree, BinaryOperation, Predicate

# Custom operation type
def custom_op(a: int, b: int) -> int:
    return a ^ b  # XOR operation

# Create typed segment tree
tree: SegmentTree[int] = SegmentTree(5, 0, custom_op)

# Predicate for binary search
predicate: Predicate[int] = lambda x: x < 100
result: int = tree.max_right(0, predicate)
```

## Integration Examples

### With NumPy
```python
import numpy as np
from segee import SumSegmentTree

# Convert NumPy array to segment tree
arr = np.array([1, 2, 3, 4, 5])
tree = SumSegmentTree(len(arr))
for i, val in enumerate(arr):
    tree.set(i, val)
```

### With Pandas
```python
import pandas as pd
from segee import SumSegmentTree

# Process DataFrame with segment tree
df = pd.DataFrame({'values': [10, 20, 30, 40, 50]})
tree = SumSegmentTree(len(df))
for i, val in enumerate(df['values']):
    tree.set(i, val)

# Range queries on DataFrame indices
range_sum = tree.sum(0, 3)  # Sum of first 3 values
```

### Competitive Programming Template
```python
from segee import SumSegmentTree, MinSegmentTree

def solve():
    n, q = map(int, input().split())
    arr = list(map(int, input().split()))
    
    # Initialize segment tree
    tree = SumSegmentTree(n)
    for i, val in enumerate(arr):
        tree.set(i, val)
    
    # Process queries
    for _ in range(q):
        query_type, *args = map(int, input().split())
        if query_type == 1:  # Update
            tree.set(args[0], args[1])
        else:  # Query
            print(tree.sum(args[0], args[1]))

if __name__ == "__main__":
    solve()
```