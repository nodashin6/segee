# API Reference

## Segment Trees

### GenericSegmentTree[T]

Generic segment tree implementation supporting any associative binary operation.

```python
class GenericSegmentTree[T](size: int, identity: T, operation: BinaryOperation[T])
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

### Specialized Segment Trees

#### SumSegmentTree

Specialized segment tree for sum operations with `int | float` types.

```python
class SumSegmentTree(GenericSegmentTree[int | float])
```

**Additional Methods:**
- **`sum(left: int = 0, right: int | None = None) -> int | float`**
  Alias for `prod()` with better readability for sum operations.

- **`total() -> int | float`**
  Alias for `all_prod()` returning sum of all elements.

- **`prefix_sum(right: int) -> int | float`**
  Sum of elements from index 0 to right-1 (inclusive).

- **`identity: int | float`** - Returns 0 (identity for addition)

#### MinSegmentTree

Specialized segment tree for minimum operations with `int | float` types.

```python
class MinSegmentTree(GenericSegmentTree[int | float])
```

**Additional Methods:**
- **`minimum(left: int = 0, right: int | None = None) -> int | float`**
  Find minimum element in specified range.

- **`global_min() -> int | float`**
  Find minimum element in entire tree.

#### MaxSegmentTree

Specialized segment tree for maximum operations with `int | float` types.

```python
class MaxSegmentTree(GenericSegmentTree[int | float])
```

**Additional Methods:**
- **`maximum(left: int = 0, right: int | None = None) -> int | float`**
  Find maximum element in specified range.

- **`global_max() -> int | float`**
  Find maximum element in entire tree.

## Binary Indexed Trees

### GenericBinaryIndexedTree[T: AdditiveProtocol]

Generic binary indexed tree for types supporting additive operations.

```python
class GenericBinaryIndexedTree[T: AdditiveProtocol](data: int | Sequence[T] = 0)
```

#### Parameters
- **data** (`int | Sequence[T]`): Size (initialized with zeros) or initial sequence

#### Methods

##### Core Operations
- **`add(index: int, value: T) -> None`**
  Add value to element at specified index.

- **`set(index: int, value: T) -> None`**
  Set element at specified index to specific value.

- **`get(index: int) -> T`**
  Get element at specified index.

- **`prefix_sum(right: int) -> T`**
  Sum of elements from index 0 to right-1 (inclusive).

- **`sum(left: int = 0, right: int | None = None) -> T`**
  Sum of elements in range [left, right).

- **`total() -> T`**
  Sum of all elements.

##### Properties
- **`size: int`** - Number of elements in the tree
- **`identity: T`** - Identity element (0)

#### Sequence Protocol
- **`__len__() -> int`** - Returns tree size
- **`__getitem__(index: int) -> T`** - Get element
- **`__setitem__(index: int, value: T) -> None`** - Set element
- **`__iter__() -> Iterator[T]`** - Iterate over elements
- **`to_list() -> list[T]`** - Convert to Python list

### GenericRangeAddBinaryIndexedTree[T: AdditiveProtocol]

Generic range-updatable binary indexed tree using dual-BIT technique.

```python
class GenericRangeAddBinaryIndexedTree[T: AdditiveProtocol](data: int | Sequence[T] = 0)
```

#### Methods

##### Core Operations
- **`add(left: int, right: int | None, *, value: T) -> None`**
  Add value to all elements in range [left, right).

- **`get(index: int) -> T`**
  Get current value at specified index.

- **`prefix_sum(right: int) -> T`**
  Sum of elements from index 0 to right-1 (inclusive).

- **`sum(left: int = 0, right: int | None = None) -> T`**
  Sum of elements in range [left, right).

##### Properties
- **`size: int`** - Number of elements in the tree
- **`identity: T`** - Identity element (0)

### Specialized Binary Indexed Trees

#### BinaryIndexedTree

Specialized binary indexed tree for `int | float` types.

```python
class BinaryIndexedTree(GenericBinaryIndexedTree[int | float])
```

#### RangeAddBinaryIndexedTree

Specialized range-updatable binary indexed tree for `int | float` types.

```python
class RangeAddBinaryIndexedTree(GenericRangeAddBinaryIndexedTree[int | float])
```

## Protocol System

### AdditiveProtocol

Protocol for types supporting addition and subtraction operations.

```python
class AdditiveProtocol(Protocol):
    def __add__(self, other: Self) -> Self: ...
    def __sub__(self, other: Self) -> Self: ...
```

**Compatible Types:** `int`, `float`, `Decimal`, `complex`, custom numeric types

### ComparableProtocol

Protocol for types supporting comparison operations.

```python
class ComparableProtocol(Protocol):
    def __lt__(self, other: Self) -> bool: ...
    def __le__(self, other: Self) -> bool: ...
    def __gt__(self, other: Self) -> bool: ...
    def __ge__(self, other: Self) -> bool: ...
```

**Compatible Types:** `int`, `float`, `str`, `datetime`, any comparable type

### MultiplicativeProtocol

Protocol for types supporting multiplication and division operations.

```python
class MultiplicativeProtocol(Protocol):
    def __mul__(self, other: Self) -> Self: ...
    def __truediv__(self, other: Self) -> Self: ...
```

**Compatible Types:** `int`, `float`, `Decimal`, `complex`, matrices

## Query Mixins

### RangeSumQueryMixin[T]

Mixin providing standardized sum query interface.

```python
class RangeSumQueryMixin[T](ABC):
    @property
    @abstractmethod
    def identity(self) -> T: ...

    @abstractmethod
    def prefix_sum(self, right: int) -> T: ...

    def sum(self, left: int = 0, right: int | None = None) -> T: ...
```

### RangeMinQueryMixin[T]

Mixin providing standardized minimum query interface.

```python
class RangeMinQueryMixin[T](ABC):
    @abstractmethod
    def minimum(self, left: int = 0, right: int | None = None) -> T: ...

    def global_min(self) -> T: ...
```

### RangeMaxQueryMixin[T]

Mixin providing standardized maximum query interface.

```python
class RangeMaxQueryMixin[T](ABC):
    @abstractmethod
    def maximum(self, left: int = 0, right: int | None = None) -> T: ...

    def global_max(self) -> T: ...
```

### PointAddQueryMixin

Mixin providing standardized point addition interface.

```python
class PointAddQueryMixin(ABC):
    @abstractmethod
    def add(self, index: int, value: T) -> None: ...
```

### RangeAddQueryMixin[T]

Mixin providing standardized range addition interface.

```python
class RangeAddQueryMixin[T](ABC):
    @abstractmethod
    def add(self, left: int, right: int, value: T) -> None: ...

    @abstractmethod
    def get(self, index: int) -> T: ...
```

## Exception Hierarchy

### SegmentTreeError

Base exception class for all segment tree related errors.

```python
class SegmentTreeError(Exception): ...
```

### SegmentTreeInitializationError

Raised when segment tree initialization fails.

```python
class SegmentTreeInitializationError(SegmentTreeError): ...
```

### SegmentTreeIndexError

Raised when accessing invalid indices.

```python
class SegmentTreeIndexError(SegmentTreeError):
    def __init__(self, index: int, size: int): ...

    @property
    def index(self) -> int: ...

    @property
    def size(self) -> int: ...
```

### SegmentTreeRangeError

Raised when using invalid ranges.

```python
class SegmentTreeRangeError(SegmentTreeError):
    def __init__(self, left: int, right: int, size: int): ...

    @property
    def left(self) -> int: ...

    @property
    def right(self) -> int: ...

    @property
    def size(self) -> int: ...
```

### BinaryIndexedTreeError

Base exception class for binary indexed tree related errors.

```python
class BinaryIndexedTreeError(SegmentTreeError): ...
```

## Type Aliases

### Common Type Aliases

```python
# Binary operation type
BinaryOperation = Callable[[T, T], T]

# Predicate type for binary search
Predicate = Callable[[T], bool]

# Sequence type for initialization
InitSequence = int | Sequence[T]
```

## Constants and Utilities

### Version Information

```python
__version__: str  # Package version from pyproject.toml
```

### Imports

```python
# Main classes
from segee import (
    GenericSegmentTree,
    SumSegmentTree,
    MinSegmentTree,
    MaxSegmentTree,
    GenericBinaryIndexedTree,
    BinaryIndexedTree,
    GenericRangeAddBinaryIndexedTree,
    RangeAddBinaryIndexedTree,
)

# Protocols
from segee.shared.protocols import (
    AdditiveProtocol,
    ComparableProtocol,
    MultiplicativeProtocol,
)

# Query mixins
from segee.shared.queries import (
    RangeSumQueryMixin,
    RangeMinQueryMixin,
    RangeMaxQueryMixin,
    PointAddQueryMixin,
    RangeAddQueryMixin,
)

# Exceptions
from segee import (
    SegmentTreeError,
    SegmentTreeInitializationError,
    SegmentTreeIndexError,
    SegmentTreeRangeError,
    BinaryIndexedTreeError,
)
```
