# AGENTS.md

This file contains guidelines for agentic coding agents working in this repository.

## Project Overview

This is a Python package for querying RISM Online data. The package uses modern Python practices with UV as the package manager and focuses on type-safe, immutable domain objects.

## Development Commands

### Package Management
```bash
# Install dependencies
uv sync

# Add new dependency
uv add <package-name>

# Run the application
uv run python main.py

# Run as module
uv run python -m rism
```

### Testing (Currently Not Set Up)
```bash
# Install test dependencies (needs to be added)
uv add --dev pytest pytest-cov

# Run all tests
uv run pytest

# Run single test file
uv run pytest tests/test_client.py

# Run specific test
uv run pytest tests/test_client.py::test_search_sources

# Run with coverage
uv run pytest --cov=rism
```

### Code Quality (Currently Not Set Up)
```bash
# Install linting dependencies (needs to be added)
uv add --dev ruff black isort mypy

# Format code
uv run black .
uv run isort .

# Lint code
uv run ruff check .
uv run mypy rism/
```

## Code Style Guidelines

### Import Organization
Follow PEP 8 import order:
1. Standard library imports
2. Third-party imports  
3. Local imports

```python
# Standard library
from typing import List, Optional, Dict
from dataclasses import dataclass, field

# Third-party
import requests

# Local
from .client import RISMClient
from .models.base import RISMEntry
```

### Class Design Patterns
- **Use dataclasses with `frozen=True`** for all domain objects to ensure immutability
- **Inherit from `RISMEntry`** for all domain entities
- **Use `@property` decorators** for computed fields
- **Use `field(init=False)`** for derived fields set in `__post_init__`

```python
@dataclass(frozen=True)
class RISMSource(RISMEntry):
    @property
    def title(self) -> Optional[str]:
        return self.raw.get("title")
```

### Type Safety Requirements
- **All functions must have type hints** for parameters and return values
- **Use Optional[T]** for nullable fields
- **Use List[T] and Dict[K, V]** for collections
- **Prefer specific types over generic Any**

### Naming Conventions
- **Classes**: PascalCase (RISMClient, RISMSource)
- **Functions/Methods**: snake_case (search_sources, parse_rism_entry)
- **Constants**: UPPER_SNAKE_CASE (BASE_URL, HEADERS)
- **Variables**: snake_case (query, rows, page)
- **Private fields**: Leading underscore for internal use

### Error Handling Patterns
- **HTTP errors**: Use `resp.raise_for_status()` for API calls
- **Validation**: Raise ValueError for invalid input in `__post_init__`
- **Type errors**: Raise TypeError for type mismatches
- **Graceful defaults**: Use `.get()` with default values for optional JSON fields

```python
resp = self.session.get(url, params=params)
resp.raise_for_status()  # Handle HTTP errors

# Graceful handling of optional fields
title = item.get("title", "No title")
```

### API Client Design
- **Use requests.Session** for connection reuse and consistent headers
- **Define constants** at module level for base URLs and headers
- **Return typed objects** instead of raw dictionaries
- **Use keyword arguments** for optional parameters with sensible defaults

### Documentation Standards
- **Docstrings**: Use minimal but clear docstrings for classes and public methods
- **Type hints**: Comprehensive use of typing module is required
- **Comments**: Keep comments minimal - code should be self-documenting

### File Organization
```
rism/
├── client.py              # API client classes
├── models/
│   ├── __init__.py       # Model exports
│   ├── base.py           # Base classes
│   ├── entities.py       # Domain entities
│   ├── collections.py    # Collection classes
│   └── factory.py        # Factory functions
└── __init__.py           # Package exports
```

## Architecture Principles

### Immutability
All domain objects must be immutable using `@dataclass(frozen=True)`. This ensures thread safety and predictable behavior.

### Type Safety
Heavy use of the typing module is required. All public APIs must have complete type annotations.

### Minimal Dependencies
Keep dependencies minimal. Currently only `requests` is used for HTTP functionality.

### Factory Pattern
Use factory functions for object creation from raw data. Centralize parsing logic in the factory module.

## Testing Guidelines

### Test Structure (When Added)
- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use descriptive test names that explain the scenario
- Mock external API calls using `pytest.mock`

### Test Coverage
- Aim for >90% code coverage
- Test all public methods
- Test error conditions and edge cases
- Test type validation in `__post_init__` methods

## Development Workflow

1. **Before making changes**: Run existing tests to ensure green build
2. **Make changes**: Follow all code style guidelines
3. **Test changes**: Run relevant tests and ensure coverage
4. **Lint code**: Run ruff and mypy to check for issues
5. **Format code**: Run black and isort for consistent formatting

## Common Patterns

### Property-based Access
Use properties for clean field access to raw data:

```python
@property
def composers(self) -> List[Dict]:
    return self.raw.get("composer", [])
```

### Session Management
Initialize session with headers in constructor:

```python
def __init__(self):
    self.session = requests.Session()
    self.session.headers.update(HEADERS)
```

### Error Handling
Handle HTTP errors gracefully and provide meaningful error messages:

```python
resp = self.session.get(url, params=params)
resp.raise_for_status()
```

## Package Configuration

This project uses UV as the package manager. All dependencies are managed through `pyproject.toml`. The package supports Python 3.12+.

When adding new dependencies, use:
```bash
uv add <package-name>          # Runtime dependency
uv add --dev <package-name>    # Development dependency
```