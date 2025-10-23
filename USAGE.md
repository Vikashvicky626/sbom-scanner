# SBOM Scanner - Usage Guide

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Advanced Usage](#advanced-usage)
4. [Configuration](#configuration)
5. [Output Formats](#output-formats)
6. [Integration Examples](#integration-examples)
7. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from source

```bash
git clone https://github.com/yourusername/sbom-scanner.git
cd sbom-scanner
pip install -r requirements.txt
pip install -e .
```

### Verify installation

```bash
sbom-scan --version
```

## Basic Usage

### Scan current directory

```bash
sbom-scan
```

Output: `sbom.json` in current directory

### Scan specific directory

```bash
sbom-scan /path/to/project
```

### Custom output file

```bash
sbom-scan -o my-sbom.json
```

### XML format output

```bash
sbom-scan -f xml -o sbom.xml
```

## Advanced Usage

### Full command with all options

```bash
sbom-scan /path/to/project \
  --output sbom.json \
  --format json \
  --project-name "MyApplication" \
  --project-version "2.1.0" \
  --min-confidence 0.85 \
  --verbose
```

### Strict mode (fewer false positives)

```bash
sbom-scan --min-confidence 0.95
```

### Permissive mode (catch all dependencies)

```bash
sbom-scan --min-confidence 0.7
```

### Scan and pipe to another tool

```bash
sbom-scan -o - | jq '.components | length'
```

## Configuration

### Environment Variables

Set default behavior using environment variables:

```bash
export SBOM_MIN_CONFIDENCE=0.85
export SBOM_OUTPUT_FORMAT=json
export SBOM_VERBOSE=true
```

### Config File (Future Enhancement)

Create `.sbom-scanner.yaml` in project root:

```yaml
min_confidence: 0.8
output:
  format: json
  path: sbom.json
project:
  name: MyProject
  version: 1.0.0
```

## Output Formats

### JSON (CycloneDX 1.5)

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "version": 1,
  "metadata": {
    "component": {
      "type": "application",
      "name": "my-project",
      "version": "1.0.0"
    }
  },
  "components": [...]
}
```

### XML (CycloneDX 1.5)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bom xmlns="http://cyclonedx.org/schema/bom/1.5">
  <metadata>
    <component type="application">
      <name>my-project</name>
      <version>1.0.0</version>
    </component>
  </metadata>
  <components>...</components>
</bom>
```

## Integration Examples

### GitHub Actions

```yaml
name: Generate SBOM
on: [push]

jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install SBOM Scanner
        run: pip install sbom-scanner
      
      - name: Generate SBOM
        run: sbom-scan -o sbom.json -n "${{ github.repository }}" -v "${{ github.sha }}"
      
      - name: Upload SBOM
        uses: actions/upload-artifact@v3
        with:
          name: sbom
          path: sbom.json
```

### GitLab CI

```yaml
sbom:
  image: python:3.11
  script:
    - pip install sbom-scanner
    - sbom-scan -o sbom.json -n "$CI_PROJECT_NAME" -v "$CI_COMMIT_SHA"
  artifacts:
    paths:
      - sbom.json
```

### Jenkins

```groovy
pipeline {
    agent any
    stages {
        stage('Generate SBOM') {
            steps {
                sh 'pip install sbom-scanner'
                sh 'sbom-scan -o sbom.json'
                archiveArtifacts artifacts: 'sbom.json'
            }
        }
    }
}
```

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /scan

RUN pip install sbom-scanner

ENTRYPOINT ["sbom-scan"]
CMD ["."]
```

Build and run:

```bash
docker build -t sbom-scanner .
docker run -v $(pwd):/scan sbom-scanner -o /scan/sbom.json
```

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
echo "Generating SBOM..."
sbom-scan -o sbom.json

if [ $? -eq 0 ]; then
    echo "✓ SBOM generated successfully"
    git add sbom.json
else
    echo "✗ SBOM generation failed"
    exit 1
fi
```

### Makefile

```makefile
.PHONY: sbom
sbom:
	@echo "Generating SBOM..."
	sbom-scan -o sbom.json -n "$(PROJECT_NAME)" -v "$(VERSION)"
	@echo "SBOM saved to sbom.json"

.PHONY: sbom-xml
sbom-xml:
	@echo "Generating SBOM (XML)..."
	sbom-scan -o sbom.xml -f xml -n "$(PROJECT_NAME)" -v "$(VERSION)"
	@echo "SBOM saved to sbom.xml"
```

## Troubleshooting

### Problem: No dependencies found

**Solution:**
- Verify manifest files exist in the project
- Check if project root is being scanned
- Try with `--verbose` flag for detailed output
- Lower confidence threshold: `--min-confidence 0.7`

### Problem: Too many false positives

**Solution:**
- Increase confidence threshold: `--min-confidence 0.9`
- Check if scanning from correct directory
- Verify manifest files are not in `node_modules`, `vendor`, etc.

### Problem: Module import errors

**Solution:**
```bash
pip install --upgrade sbom-scanner
pip install -r requirements.txt
```

### Problem: XML parsing errors (Maven/NuGet)

**Solution:**
- Validate XML files are well-formed
- Check for special characters in XML
- Ensure proper encoding (UTF-8)

### Problem: Permission denied

**Solution:**
```bash
# Linux/Mac
chmod +x $(which sbom-scan)

# Or run with python
python -m sbom_scanner.cli
```

### Problem: Large projects take too long

**Solution:**
- Scanner is optimized for large projects
- Skips vendor directories automatically
- Consider scanning specific subdirectories
- Use `--verbose` to see progress

### Problem: Version specifiers not recognized

**Solution:**
- Scanner normalizes most version formats
- Some exotic version specs may not parse correctly
- File an issue with examples on GitHub

## Performance Tips

### For large monorepos

```bash
# Scan specific directories
sbom-scan ./backend -o backend-sbom.json
sbom-scan ./frontend -o frontend-sbom.json
```

### Skip unnecessary directories

Automatically skipped:
- `node_modules`, `vendor`, `bower_components`
- `.git`, `.svn`, `.hg`
- `venv`, `env`, `virtualenv`
- `target`, `build`, `dist`
- `__pycache__`, `.pytest_cache`

### Parallel scanning

```bash
# Scan multiple projects in parallel
sbom-scan ./project1 -o sbom1.json &
sbom-scan ./project2 -o sbom2.json &
wait
```

## API Usage

### Python API

```python
from sbom_scanner.scanner import Scanner
from sbom_scanner.cyclonedx_generator import CycloneDXGenerator

# Initialize
scanner = Scanner(min_confidence=0.8)

# Scan
result = scanner.scan(
    path="/path/to/project",
    project_name="MyProject",
    project_version="1.0.0"
)

# Generate SBOM
generator = CycloneDXGenerator()
sbom_json = generator.generate(result, "json")

# Save to file
generator.save_to_file(result, "sbom.json", "json")

# Access dependencies
for dep in result.dependencies:
    print(f"{dep.name}@{dep.version}")
```

### Custom filtering

```python
from sbom_scanner.models import Ecosystem, DependencyType

# Filter by ecosystem
npm_deps = [d for d in result.dependencies 
            if d.ecosystem == Ecosystem.NPM]

# Filter by type
prod_deps = [d for d in result.dependencies 
             if d.dependency_type == DependencyType.DIRECT]

# Filter by confidence
high_conf = [d for d in result.dependencies 
             if d.confidence >= 0.95]
```

## Best Practices

1. **Version Control**: Commit generated SBOMs to track dependency changes
2. **CI/CD**: Generate SBOMs on every build
3. **Security**: Feed SBOMs to vulnerability scanners
4. **Compliance**: Use for license compliance tracking
5. **Documentation**: Include SBOM in release artifacts
6. **Monitoring**: Track dependency count trends over time

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/sbom-scanner/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/sbom-scanner/discussions)
- **Email**: support@example.com

