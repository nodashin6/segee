# API Reference

## Core Classes

### SegmentTree

Generic segment tree implementation supporting any associative binary operation.

```python
class SegmentTree[T](size: int, identity: T, operation: BinaryOperation[T])
```

#### Parameters
- **size** (`int`): Number of elements the tree can hold (must be > 0)
- **identity** (`T`): Identity element for the operation (e.g., 0 for sum, ∞ for min)
- **operation** (`BinaryOperation[T]`): Associative binary operation

#### Methods

##### Core Operations
- **`set(index: int, value: T) -> None`**  
  Update element at specified index. Supports negative indexing.

- **`get(index: int) -> T`**  
  Retrieve element at specified index. Supports negative indexing.

- **`prod(left: int = 0, right: int | None = None) -> T`**  
  Query range [left, right). If right is None, queries to end of tree.

- **`all_prod() -> T`**  
  Query the entire range [0, size).

##### Binary Search Operations
- **`max_right(left: int, predicate: Predicate[T]) -> int`**  
  Find maximum r such that predicate(prod(left, r)) is True.

- **`min_left(right: int, predicate: Predicate[T]) -> int`**  
  Find minimum l such that predicate(prod(l, right)) is True.

##### Properties
- **`size: int`** - Number of elements in the tree

#### Sequence Protocol
- **`__len__() -> int`** - Returns tree size
- **`__getitem__(index: int | slice) -> T | list[T]`** - Get element(s)  
- **`__setitem__(index: int, value: T) -> None`** - Set element
- **`__contains__(value: T) -> bool`** - Check membership
- **`__iter__() -> Iterator[T]`** - Iterate over elements
- **`__eq__(other: object) -> bool`** - Equality comparison

## Specialized Classes

### SumSegmentTree

Convenience class for sum operations.

```python
class SumSegmentTree(size: int)
```

#### Additional Methods
- **`sum(left: int = 0, right: int | None = None) -> int | float`**  
  Alias for `prod()` - returns sum of range [left, right).

- **`total() -> int | float`**  
  Alias for `all_prod()` - returns sum of all elements.

### MinSegmentTree

Convenience class for minimum operations.

```python
class MinSegmentTree(size: int)
```

#### Additional Methods
- **`minimum(left: int = 0, right: int | None = None) -> int | float`**  
  Alias for `prod()` - returns minimum of range [left, right).

- **`global_min() -> int | float`**  
  Alias for `all_prod()` - returns minimum of all elements.

### MaxSegmentTree

Convenience class for maximum operations.

```python
class MaxSegmentTree(size: int)
```

#### Additional Methods
- **`maximum(left: int = 0, right: int | None = None) -> int | float`**  
  Alias for `prod()` - returns maximum of range [left, right).

- **`global_max() -> int | float`**  
  Alias for `all_prod()` - returns maximum of all elements.

## Exception Classes

### SegmentTreeError

Base exception class for all segment tree errors.

```python
class SegmentTreeError(Exception)
```

### SegmentTreeIndexError

Raised when accessing invalid indices.

```python
class SegmentTreeIndexError(SegmentTreeError)
```

#### Attributes
- **`index: int`** - The invalid index that was accessed
- **`size: int`** - The size of the segment tree

### SegmentTreeRangeError

Raised when querying invalid ranges.

```python
class SegmentTreeRangeError(SegmentTreeError)
```

#### Attributes
- **`left: int`** - The left bound of the invalid range
- **`right: int`** - The right bound of the invalid range  
- **`size: int`** - The size of the segment tree

### SegmentTreeInitializationError

Raised when creating segment tree with invalid parameters.

```python
class SegmentTreeInitializationError(SegmentTreeError, ValueError)
```

## Type Definitions

### BinaryOperation

Type alias for binary operations.

```python
BinaryOperation[T] = Callable[[T, T], T]
```

Example operations:
- `operator.add` - Addition
- `operator.mul` - Multiplication  
- `min` - Minimum
- `max` - Maximum
- `math.gcd` - Greatest common divisor
- `operator.xor` - XOR operation

### Predicate

Type alias for predicate functions used in binary search.

```python
Predicate[T] = Callable[[T], bool]
```

Examples:
- `lambda x: x <= threshold` - Check if value is at most threshold
- `lambda x: x >= target` - Check if value is at least target
- `lambda x: x == expected` - Check equality

## Complexity Analysis

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Initialization | O(n) | O(n) |
| `set(index, value)` | O(log n) | O(1) |
| `get(index)` | O(1) | O(1) |
| `prod(left, right)` | O(log n) | O(1) |
| `max_right(left, pred)` | O(log² n) | O(1) |
| `min_left(right, pred)` | O(log² n) | O(1) |

## Implementation Details

### Tree Structure
- Uses a complete binary tree stored in an array
- Internal nodes store aggregated values
- Leaf nodes store actual data values
- Tree size is rounded up to next power of 2 internally

### Memory Layout
```
Tree with size=5, internally uses array of size=16:

Index:  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
Level:  0   1   1   2   2   2   2   3   3   3   3   3   3   3   3
Data:   *   *   *   *   *   *   *   a   b   c   d   e   -   -   -

Where a,b,c,d,e are the 5 data elements, * are internal aggregated values
```

### Operation Properties

For correct behavior, operations must be:
- **Associative**: `op(op(a, b), c) = op(a, op(b, c))`
- **Have identity**: `op(identity, a) = op(a, identity) = a`

Examples of valid operations:
- Addition with identity 0
- Multiplication with identity 1  
- Min with identity +∞
- Max with identity -∞
- GCD with identity 0
- String concatenation with identity ""

## Usage Patterns

### Pattern 1: Range Sum Queries
```python
# Perfect for problems like "sum of elements in range [l, r]"
tree = SumSegmentTree(n)
for i, val in enumerate(initial_array):
    tree.set(i, val)

# Process queries
for left, right in query_ranges:
    result = tree.sum(left, right)
```

### Pattern 2: Range Minimum Queries  
```python
# Perfect for problems like "minimum element in range [l, r]"
tree = MinSegmentTree(n)
for i, val in enumerate(initial_array):
    tree.set(i, val)

# Process queries
for left, right in query_ranges:
    result = tree.minimum(left, right)
```

### Pattern 3: Binary Search on Prefix/Suffix
```python
# Find longest prefix with property P
tree = SumSegmentTree(n)
# ... set values ...

# Find maximum right where cumulative sum <= threshold
pos = tree.max_right(0, lambda cumsum: cumsum <= threshold)
```

### Pattern 4: Custom Operations
```python
# Example: Range GCD queries
import math
tree = SegmentTree(n, 0, math.gcd)

# Example: Range bitwise OR queries  
tree = SegmentTree(n, 0, operator.or_)
```