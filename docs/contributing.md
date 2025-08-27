# Contributing to Segee

Thank you for your interest in contributing to Segee! This guide will help you contribute to our enterprise-grade data structures library.

## Development Setup

### Prerequisites
- Python 3.12 or higher
- Git

### Clone and Setup
```bash
git clone https://github.com/nodashin/segee.git
cd segee
pip install -e ".[dev]"
```

### Development Dependencies
The `dev` extra includes:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting  
- `mypy` - Static type checking
- `ruff` - Code formatting and linting
- `pre-commit` - Git hooks for code quality

## Code Quality Standards

### Formatting
We use Ruff for code formatting:
```bash
# Format code
ruff format

# Check and fix linting issues
ruff check --fix
```

### Type Checking
All code must pass mypy strict mode:
```bash
mypy segee/
```

### Testing
Comprehensive test coverage is required:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=segee --cov-report=html

# Run specific test categories
pytest tests/segment_tree/core/     # Core functionality
pytest tests/segment_tree/application/  # Specialized classes
pytest tests/samples/               # Real-world examples
```

## Project Structure

```
segee/
├── segment_tree/           # Segment tree module
│   ├── backbone/          # Generic implementations
│   │   └── generic_segment_tree.py
│   ├── specialized/       # Specialized classes (Sum/Min/Max)
│   └── __init__.py       # Module exports
├── binary_indexed_tree/   # Binary indexed tree module
│   ├── backbone/          # Generic implementations
│   │   ├── generic_binary_indexed_tree.py
│   │   └── generic_range_updatable_binary_indexed_tree.py
│   ├── specialized/       # Specialized classes
│   └── __init__.py       # Module exports
├── shared/               # Shared components
│   ├── backbone/         # Base classes and mixins
│   ├── protocols/        # Type protocols (AdditiveProtocol, etc.)
│   └── queries/          # Query mixins (RangeSumQuery, etc.)
├── cli.py               # Legacy CLI entry point
├── exceptions.py        # Custom exception hierarchy
└── __init__.py         # Package exports

segee_cli/              # Interactive CLI application
├── main.py            # CLI implementation
└── __init__.py        # CLI exports

tests/
├── segment_tree/       # Segment tree tests (152 tests)
│   ├── core/          # Basic functionality
│   └── application/   # Specialized classes
├── binary_indexed_tree/  # Binary indexed tree tests (80 tests)
├── samples/           # Real-world problem examples
│   ├── 01_range_sum_query/
│   ├── 02_range_min_query/
│   └── performance_test.py
└── test_*.py         # Exception and protocol tests

docs/
├── usage.md          # Comprehensive usage guide
├── api.md           # Complete API reference
├── performance.md   # Performance analysis
└── contributing.md  # This file
```

## Contributing Guidelines

### 1. Code Style
- Follow PEP 8 and Ruff formatting
- Use type hints for all public APIs
- Write clear, descriptive docstrings
- Keep functions focused and modular

### 2. Testing Requirements
- Write tests for all new functionality
- Maintain comprehensive test coverage (currently 232 tests)
- Include edge cases and error conditions
- Add performance tests for new algorithms
- Follow the backbone/specialized testing pattern

### 3. Documentation
- Update API documentation for new methods
- Add usage examples for new features
- Update README if adding major functionality
- Include docstrings with Google style

### 4. Git Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ... code, test, document ...

# Run quality checks
ruff format
ruff check --fix
mypy segee/
pytest

# Commit your changes
git add .
git commit -m "Add your feature description"

# Push and create PR
git push origin feature/your-feature-name
```

## Types of Contributions

### 🐛 Bug Fixes
- Fix issues in existing functionality
- Add regression tests
- Update documentation if behavior changes

### ✨ New Features
- Add new segment tree or binary indexed tree variants
- Implement additional operations and protocols
- Extend binary search functionality
- Create new query mixins for standardized interfaces
- Implement lazy propagation for segment trees

### 📚 Documentation
- Improve usage examples
- Add performance guides
- Create tutorials for specific use cases

### 🔧 Infrastructure
- Improve build system
- Add CI/CD enhancements
- Optimize development workflow

## Testing Strategy

### Test Categories

1. **Core Tests** (`tests/segment_tree/core/`, `tests/binary_indexed_tree/core/`)
   - Basic operations (set, get, prod, sum)
   - Binary search methods (max_right, min_left) for segment trees
   - Edge cases and error conditions
   - Protocol implementations

2. **Application Tests** (`tests/segment_tree/application/`, `tests/binary_indexed_tree/application/`)
   - Specialized classes (Sum/Min/Max segment trees, BIT variants)
   - Query mixin integration
   - Convenience methods and aliases
   - Class-specific functionality

3. **Sample Tests** (`tests/samples/`)
   - Real-world problem scenarios
   - Ground truth validation with naive solutions
   - Performance comparisons between data structures

4. **Shared Component Tests** (`tests/test_protocols.py`, `tests/test_queries.py`)
   - Protocol implementations
   - Query mixin functionality
   - Shared backbone components

### Writing Tests

```python
class TestYourFeature:
    """Test your new feature following enterprise patterns."""
    
    def test_basic_functionality(self) -> None:
        """Test basic functionality works correctly."""
        # Test both data structures when applicable
        seg_tree = SumSegmentTree(5)
        seg_tree.set(0, 10)
        assert seg_tree.sum(0, 1) == 10
        
        bit = BinaryIndexedTree([10, 0, 0, 0, 0])
        assert bit.sum(0, 1) == 10
    
    def test_protocol_compliance(self) -> None:
        """Test protocol implementations."""
        from segee.shared.protocols import AdditiveProtocol
        tree = GenericBinaryIndexedTree[int](5)
        assert isinstance(1, AdditiveProtocol)  # Type checking
    
    def test_mixin_integration(self) -> None:
        """Test query mixin functionality."""
        tree = SumSegmentTree(5)
        assert hasattr(tree, 'sum')  # From RangeSumQueryMixin
        assert hasattr(tree, 'prefix_sum')
    
    def test_error_conditions(self) -> None:
        """Test proper error handling."""
        tree = SumSegmentTree(5)
        with pytest.raises(SegmentTreeIndexError):
            tree.get(10)
```

### Adding Sample Problems

To add a new sample problem:

1. Create directory `tests/samples/XX_problem_name/`
2. Add `problem.md` with problem description
3. Create `solve.py` with segment tree solution  
4. Create `groundtruth.py` with naive O(n) solution
5. Add `test_solution.py` with comprehensive tests

Example structure:
```
tests/samples/03_your_problem/
├── problem.md              # Problem description
├── solve.py               # Segment tree solution
├── groundtruth.py         # Naive solution for validation
└── test_solution.py       # Test cases and comparisons
```

## Code Review Process

### Before Submitting PR
- [ ] All tests pass (`pytest`)
- [ ] Code is formatted (`ruff format`)
- [ ] No linting errors (`ruff check`)
- [ ] Type checking passes (`mypy segee/`)
- [ ] Documentation is updated
- [ ] Changelog entry added (if applicable)

### PR Requirements
- Clear description of changes
- Reference to related issues
- Test coverage for new code
- Performance impact assessment (if applicable)

## Release Process

### Version Numbering
We follow [Semantic Versioning](https://semver.org/):
- **Major** (X.0.0): Breaking changes
- **Minor** (0.X.0): New features, backward compatible
- **Patch** (0.0.X): Bug fixes, backward compatible

### Release Checklist
- [ ] Update version in `pyproject.toml`
- [ ] Update changelog
- [ ] Run full test suite
- [ ] Build and test package (`pip install -e .`)
- [ ] Create git tag
- [ ] Build distribution (`python -m build`)
- [ ] Upload to PyPI (`twine upload dist/*`)

## Architecture Decisions

### Enterprise Design Patterns
The codebase follows enterprise-grade patterns:
- **Backbone/Specialized Pattern**: Generic implementations in `backbone/`, specialized in `specialized/`
- **Protocol-Based Type System**: AdditiveProtocol, ComparableProtocol for flexible constraints
- **Mixin Architecture**: Query interfaces through shared mixins
- **Comprehensive Testing**: 232 tests with ground truth validation

### Current Implementation Status
- `segee/segment_tree/` - Complete with backbone/specialized pattern
- `segee/binary_indexed_tree/` - Complete with backbone/specialized pattern
- `segee/shared/` - Protocol and mixin framework
- `segee_cli/` - Interactive CLI application

### Future Extensibility
The architecture supports future data structures:
- `segee/sparse_table/` - Potential future addition
- `segee/lazy_segment_tree/` - Lazy propagation extension
- Additional query mixins and protocols

### Design Principles
1. **Type Safety**: Complete type hints with protocol-based constraints
2. **Modular Architecture**: Clear separation between backbone and specialized implementations  
3. **Pythonic API**: Follow Python conventions with full sequence protocol support
4. **Performance**: O(log n) guarantees with memory-optimized implementations
5. **Error Handling**: Comprehensive exception hierarchy with context
6. **Testability**: Ground truth validation and performance benchmarking
7. **Extensibility**: Plugin-like mixin system for new functionality

## Getting Help

### Questions and Discussions
- Open an issue for bugs or feature requests
- Use discussions for general questions
- Check existing issues before creating new ones

### Code Review
- Be respectful and constructive
- Focus on code quality and maintainability
- Ask questions if anything is unclear
- Suggest improvements with examples

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in significant feature additions

Thank you for making Segee better! 🚀