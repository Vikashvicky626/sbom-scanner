# Contributing to SBOM Scanner

Thank you for your interest in contributing to SBOM Scanner! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Project Structure](#project-structure)
5. [Adding a New Language Detector](#adding-a-new-language-detector)
6. [Testing](#testing)
7. [Coding Standards](#coding-standards)
8. [Submitting Changes](#submitting-changes)

## Code of Conduct

Be respectful, inclusive, and professional. We value contributions from everyone.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/sbom-scanner.git`
3. Create a branch: `git checkout -b feature/my-feature`
4. Make your changes
5. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.8+
- pip
- git

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/sbom-scanner.git
cd sbom-scanner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Run tests (once tests are added)
pytest
```

## Project Structure

```
sbom-scanner/
├── sbom_scanner/           # Main package
│   ├── __init__.py
│   ├── models.py           # Data models
│   ├── scanner.py          # Core scanner
│   ├── cyclonedx_generator.py  # BOM generation
│   ├── cli.py              # CLI interface
│   └── detectors/          # Language detectors
│       ├── __init__.py
│       ├── base.py         # Base detector class
│       ├── npm_detector.py
│       ├── python_detector.py
│       └── ...
├── examples/               # Usage examples
├── tests/                  # Test files
├── requirements.txt        # Dependencies
├── setup.py               # Package setup
└── README.md
```

## Adding a New Language Detector

### Step 1: Create Detector File

Create `sbom_scanner/detectors/yourlang_detector.py`:

```python
"""
YourLang dependency detector
"""
from pathlib import Path
from typing import Set
from .base import BaseDetector
from ..models import Dependency, Ecosystem, DependencyType


class YourLangDetector(BaseDetector):
    """Detector for YourLang projects"""
    
    def get_manifest_files(self) -> list[str]:
        """Return list of manifest file names to look for"""
        return ['manifest.yml', 'dependencies.lock']
    
    def detect(self, path: Path) -> bool:
        """Check if YourLang manifest files exist"""
        return len(self.find_files(path, self.get_manifest_files())) > 0
    
    def parse(self, path: Path) -> Set[Dependency]:
        """Parse YourLang dependencies"""
        dependencies = set()
        
        manifest_files = self.find_files(path, self.get_manifest_files())
        
        for manifest_file in manifest_files:
            try:
                # Your parsing logic here
                with open(manifest_file, 'r', encoding='utf-8') as f:
                    # Parse the file
                    pass
                
                # Create Dependency objects
                dep = Dependency(
                    name="package-name",
                    version="1.0.0",
                    ecosystem=Ecosystem.UNKNOWN,  # Add your ecosystem to models.py
                    purl=f"pkg:yourlang/package-name@1.0.0",
                    dependency_type=DependencyType.DIRECT,
                    source_file=str(manifest_file.relative_to(path)),
                    confidence=1.0
                )
                dependencies.add(dep)
                
            except Exception as e:
                print(f"Warning: Could not parse {manifest_file}: {e}")
                continue
        
        return dependencies
```

### Step 2: Add Ecosystem to Models

Edit `sbom_scanner/models.py`:

```python
class Ecosystem(Enum):
    # ... existing ecosystems ...
    YOURLANG = "yourlang"
```

### Step 3: Register Detector

Edit `sbom_scanner/detectors/__init__.py`:

```python
from .yourlang_detector import YourLangDetector

__all__ = [
    # ... existing detectors ...
    'YourLangDetector',
]
```

Edit `sbom_scanner/scanner.py`:

```python
from .detectors import (
    # ... existing imports ...
    YourLangDetector,
)

class Scanner:
    def __init__(self, min_confidence: float = 0.8):
        self.detectors: List[BaseDetector] = [
            # ... existing detectors ...
            YourLangDetector(),
        ]
```

### Step 4: Add Tests

Create `tests/test_yourlang_detector.py`:

```python
import pytest
from pathlib import Path
from sbom_scanner.detectors.yourlang_detector import YourLangDetector


def test_detect(tmp_path):
    """Test detection of YourLang projects"""
    detector = YourLangDetector()
    
    # Create test manifest file
    manifest = tmp_path / "manifest.yml"
    manifest.write_text("dependencies:\n  - package: test\n")
    
    assert detector.detect(tmp_path) == True


def test_parse(tmp_path):
    """Test parsing YourLang dependencies"""
    detector = YourLangDetector()
    
    # Create test manifest
    manifest = tmp_path / "manifest.yml"
    manifest.write_text("""
dependencies:
  - name: test-package
    version: 1.0.0
""")
    
    deps = detector.parse(tmp_path)
    assert len(deps) > 0
    
    dep = list(deps)[0]
    assert dep.name == "test-package"
    assert dep.version == "1.0.0"
```

### Step 5: Update Documentation

Update `README.md` to include your new language in the supported languages table.

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sbom_scanner

# Run specific test
pytest tests/test_yourlang_detector.py
```

### Writing Tests

- Use pytest framework
- Create test fixtures for common scenarios
- Test edge cases (empty files, malformed data, etc.)
- Aim for >80% code coverage

### Test Structure

```python
import pytest
from pathlib import Path


@pytest.fixture
def sample_manifest(tmp_path):
    """Create a sample manifest file"""
    manifest = tmp_path / "manifest.json"
    manifest.write_text('{"deps": []}')
    return manifest


def test_something(sample_manifest):
    """Test description"""
    # Your test here
    assert True
```

## Coding Standards

### Python Style

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for all public methods

### Example

```python
def parse_version(version_string: str) -> str:
    """
    Parse and normalize a version string.
    
    Args:
        version_string: Raw version string from manifest
    
    Returns:
        Normalized version string
    
    Examples:
        >>> parse_version("^1.0.0")
        "1.0.0"
    """
    return version_string.lstrip('^~>=<')
```

### Imports

Group imports:

```python
# Standard library
import json
from pathlib import Path
from typing import Set

# Third-party
import click

# Local
from .base import BaseDetector
from ..models import Dependency
```

### Error Handling

- Catch specific exceptions
- Log warnings for non-critical errors
- Raise exceptions for critical errors
- Never silently ignore errors

```python
try:
    data = json.load(f)
except json.JSONDecodeError as e:
    print(f"Warning: Invalid JSON in {file_path}: {e}")
    return set()
except IOError as e:
    raise RuntimeError(f"Cannot read {file_path}: {e}")
```

## Submitting Changes

### Pull Request Process

1. **Fork and Branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make Changes**
   - Write clear, focused commits
   - Add tests for new features
   - Update documentation

3. **Test**
   ```bash
   pytest
   ```

4. **Commit**
   ```bash
   git add .
   git commit -m "Add YourLang detector"
   ```

5. **Push**
   ```bash
   git push origin feature/my-feature
   ```

6. **Create Pull Request**
   - Use clear title and description
   - Reference related issues
   - Add screenshots if applicable

### Commit Messages

Use clear, descriptive commit messages:

```
Add YourLang detector for manifest.yml files

- Implement YourLangDetector class
- Add parsing logic for manifest.yml format
- Include tests for detection and parsing
- Update documentation with new language

Fixes #123
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Added new tests
- [ ] All tests pass
- [ ] Manual testing performed

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] No linter errors
- [ ] PR title is clear
```

## Review Process

1. Maintainer reviews PR
2. Address feedback
3. Approval from maintainer
4. Merge to main

## Questions?

- Open an issue for bugs
- Use discussions for questions
- Email: dev@example.com

## Recognition

Contributors are recognized in:
- GitHub contributors page
- CHANGELOG.md
- README.md (for significant contributions)

Thank you for contributing! 🎉

