# Contributing to Segee

Thank you for your interest in contributing to Segee! This guide will help you get started.

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
├── segment_tree/           # Main implementation
│   ├── __init__.py        # Module exports
│   ├── segment_tree.py    # Generic segment tree
│   └── specialized.py     # Sum/Min/Max classes
├── exceptions.py          # Custom exceptions
├── _types.py             # Type definitions
└── __init__.py           # Package exports

tests/
├── segment_tree/          # Segment tree specific tests
│   ├── core/             # Basic functionality tests
│   └── application/      # Specialized class tests
├── samples/              # Real problem examples
│   ├── 01_range_sum_query/
│   └── 02_range_min_query/
└── test_exceptions.py    # Exception handling tests

docs/
├── usage.md              # Usage examples
├── api.md               # API documentation  
├── performance.md       # Performance guide
└── contributing.md      # This file
```

## Contributing Guidelines

### 1. Code Style
- Follow PEP 8 and Ruff formatting
- Use type hints for all public APIs
- Write clear, descriptive docstrings
- Keep functions focused and modular

### 2. Testing Requirements
- Write tests for all new functionality
- Maintain 100% test coverage
- Include edge cases and error conditions
- Add performance tests for new algorithms

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
- Add new segment tree variants
- Implement additional operations
- Extend binary search functionality

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

1. **Core Tests** (`tests/segment_tree/core/`)
   - Basic operations (set, get, prod)
   - Binary search methods (max_right, min_left)
   - Edge cases and error conditions

2. **Application Tests** (`tests/segment_tree/application/`)
   - Specialized classes (Sum/Min/MaxSegmentTree)
   - Convenience methods and aliases
   - Class-specific functionality

3. **Sample Tests** (`tests/samples/`)
   - Real-world problem scenarios
   - Ground truth validation
   - Performance comparisons

### Writing Tests

```python
class TestYourFeature:
    """Test your new feature."""
    
    def test_basic_functionality(self) -> None:
        """Test basic functionality works correctly."""
        tree = SumSegmentTree(5)
        tree.set(0, 10)
        assert tree.sum(0, 1) == 10
    
    def test_edge_cases(self) -> None:
        """Test edge cases and boundary conditions."""
        tree = SumSegmentTree(1)
        tree.set(0, 42)
        assert tree.sum() == 42
    
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

### Future Extensibility
The codebase is designed for future algorithms:
- `segee/segment_tree/` - Current implementation
- `segee/binary_indexed_tree/` - Planned addition
- `segee/sparse_table/` - Potential future addition

### Design Principles
1. **Type Safety**: Complete type hints with generic support
2. **Pythonic API**: Follow Python conventions and protocols
3. **Performance**: O(log n) guarantees with efficient implementation
4. **Error Handling**: Clear, specific exception types
5. **Testability**: Comprehensive test coverage with ground truth validation

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