# SBOM Scanner

A comprehensive multi-language dependency scanner that generates Software Bill of Materials (SBOM) in CycloneDX format with minimal false positives.

## Features

✨ **Multi-Language Support**: Automatically detects and scans dependencies from multiple programming languages and package managers

🎯 **False Positive Reduction**: Advanced filtering mechanisms to minimize false positives through confidence scoring and intelligent deduplication

📋 **CycloneDX Output**: Industry-standard SBOM format (JSON and XML) compatible with security tools and compliance frameworks

🔍 **Comprehensive Detection**: Scans all project files recursively while intelligently skipping vendor/dependency directories

⚡ **Easy to Use**: Simple CLI interface with sensible defaults

## Supported Languages & Package Managers

| Language | Package Manager | Manifest Files |
|----------|----------------|----------------|
| **JavaScript/TypeScript** | npm, yarn, pnpm | `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` |
| **Python** | pip, poetry, pipenv | `requirements.txt`, `setup.py`, `Pipfile`, `pyproject.toml` |
| **Java** | Maven, Gradle | `pom.xml`, `build.gradle`, `build.gradle.kts` |
| **PHP** | Composer | `composer.json`, `composer.lock` |
| **.NET** | NuGet | `packages.config`, `*.csproj`, `*.fsproj` |
| **Ruby** | Gem/Bundler | `Gemfile`, `Gemfile.lock` |
| **Rust** | Cargo | `Cargo.toml`, `Cargo.lock` |
| **Go** | Go Modules | `go.mod`, `go.sum` |
| **C/C++** | Conan | `conanfile.txt`, `conanfile.py`, `conan.lock` |
| **C/C++** | vcpkg | `vcpkg.json` |
| **C/C++** | CMake | `CMakeLists.txt` |
| **Embedded/IoT** | PlatformIO | `platformio.ini`, `library.json` |
| **Embedded/Arduino** | Arduino | `library.properties` |
| **Embedded/ARM** | Mbed OS | `mbed_lib.json`, `mbed.lib`, `mbed_app.json` |

## Installation

### Windows (PowerShell)

**Quick Install:**

```powershell
# Navigate to the project directory
cd D:\Projects\SBOM

# Run the installation script
.\install.ps1
```

See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for detailed Windows installation and usage instructions.

### Linux/Mac (Bash)

```bash
# Navigate to the project directory
cd /path/to/sbom-scanner

# Run the installation script
chmod +x install.sh
./install.sh
```

### From Source (All Platforms)

```bash
# Clone the repository
git clone https://github.com/yourusername/sbom-scanner.git
cd sbom-scanner

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Using pip (once published)

```bash
pip install sbom-scanner
```

## Quick Start

### Basic Usage

**Windows (PowerShell):**
```powershell
# Using the quick run script
.\run_sbom_scan.ps1

# Or using the command directly
sbom-scan
# Or if command not found:
python -m sbom_scanner.cli .
```

**Linux/Mac (Bash):**
```bash
sbom-scan
```

This will:
1. Scan the current directory for all supported dependency files
2. Extract dependencies with version information
3. Generate `sbom.json` in CycloneDX format

### Scan a Specific Directory

```bash
sbom-scan /path/to/your/project
```

### Specify Output File and Format

```bash
# Generate JSON output (default)
sbom-scan -o my-project-sbom.json

# Generate XML output
sbom-scan -o my-project-sbom.xml -f xml
```

### Add Project Metadata

```bash
sbom-scan -n "MyProject" -v "2.1.0" -o sbom.json
```

### Adjust False Positive Threshold

```bash
# Increase confidence threshold to 0.9 (more strict, fewer false positives)
sbom-scan --min-confidence 0.9

# Decrease to 0.7 (more permissive, may include more dependencies)
sbom-scan --min-confidence 0.7
```

## Command-Line Options

```
Usage: sbom-scan [OPTIONS] [PATH]

Options:
  -o, --output PATH              Output file path (default: sbom.json)
  -f, --format [json|xml]        Output format (default: json)
  -n, --project-name TEXT        Project name (defaults to directory name)
  -v, --project-version TEXT     Project version (defaults to 1.0.0)
  --min-confidence FLOAT         Minimum confidence threshold (0.0-1.0) 
                                 to reduce false positives (default: 0.8)
  --verbose                      Enable verbose output
  --version                      Show version and exit
  --help                         Show this message and exit
```

## How It Works

### 1. Project Detection

The scanner recursively searches the project directory for manifest files from all supported package managers.

### 2. Dependency Extraction

For each detected manifest file, the appropriate parser extracts:
- Package name
- Version specification
- Dependency type (direct, dev, transitive)
- Source file location

### 3. False Positive Reduction

Multiple strategies minimize false positives:

- **Confidence Scoring**: Each dependency is assigned a confidence score (0.0-1.0)
- **Directory Filtering**: Automatically skips `node_modules`, `vendor`, `.git`, `venv`, and other common dependency directories
- **Deduplication**: Removes duplicate dependencies across different manifest files
- **Version Cleaning**: Normalizes version specifiers (removes `^`, `~`, `>=`, etc.)

### 4. CycloneDX Generation

Creates a standards-compliant SBOM with:
- Component metadata (name, version, type)
- Package URLs (PURL) for each dependency
- Ecosystem information
- Relationships between components

## Example Output Structure

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
    },
    "tools": [
      {
        "name": "sbom-scanner",
        "version": "1.0.0"
      }
    ]
  },
  "components": [
    {
      "type": "library",
      "name": "express",
      "version": "4.18.2",
      "purl": "pkg:npm/express@4.18.2"
    },
    {
      "type": "library",
      "name": "requests",
      "version": "2.31.0",
      "purl": "pkg:pypi/requests@2.31.0"
    }
  ]
}
```

## Use Cases

### Security Vulnerability Scanning

Feed the generated SBOM to security tools like:
- OWASP Dependency-Track
- Anchore Grype
- Snyk
- GitHub Dependabot

```bash
sbom-scan -o sbom.json
# Upload sbom.json to your security tool
```

### Compliance & License Management

Generate SBOMs for compliance requirements (e.g., Executive Order 14028):

```bash
sbom-scan -n "ProductName" -v "1.0.0" -f xml -o sbom.xml
```

### CI/CD Integration

Add to your build pipeline:

```bash
# .github/workflows/sbom.yml
- name: Generate SBOM
  run: |
    pip install sbom-scanner
    sbom-scan -o sbom.json
    
- name: Upload SBOM
  uses: actions/upload-artifact@v3
  with:
    name: sbom
    path: sbom.json
```

### Multi-Language Projects

Perfect for polyglot projects with multiple languages:

```bash
# Project structure:
# /backend (Python)
# /frontend (JavaScript)
# /api (Java)

sbom-scan .  # Automatically detects all languages
```

## Architecture

```
sbom_scanner/
├── __init__.py           # Package initialization
├── models.py             # Data models (Dependency, ScanResult, etc.)
├── scanner.py            # Core scanner orchestration
├── cyclonedx_generator.py # CycloneDX BOM generation
├── cli.py                # Command-line interface
└── detectors/            # Language-specific detectors
    ├── __init__.py
    ├── base.py           # Base detector class
    ├── npm_detector.py   # JavaScript/Node.js
    ├── python_detector.py # Python
    ├── maven_detector.py  # Maven
    ├── gradle_detector.py # Gradle
    ├── composer_detector.py # PHP
    ├── nuget_detector.py  # .NET
    ├── ruby_detector.py   # Ruby
    ├── rust_detector.py   # Rust
    └── go_detector.py     # Go
```

## Advanced Configuration

### Programmatic Usage

```python
from sbom_scanner.scanner import Scanner
from sbom_scanner.cyclonedx_generator import CycloneDXGenerator

# Initialize scanner with custom confidence threshold
scanner = Scanner(min_confidence=0.85)

# Scan project
result = scanner.scan(
    path="/path/to/project",
    project_name="MyProject",
    project_version="2.0.0"
)

# Generate SBOM
generator = CycloneDXGenerator()
generator.save_to_file(result, "output.json", "json")

# Access dependencies programmatically
for dep in result.dependencies:
    print(f"{dep.name}@{dep.version} ({dep.ecosystem.value})")
```

### Custom Detectors

Extend the scanner with custom detectors:

```python
from sbom_scanner.detectors.base import BaseDetector
from sbom_scanner.models import Dependency, Ecosystem

class CustomDetector(BaseDetector):
    def get_manifest_files(self):
        return ['custom.lock']
    
    def detect(self, path):
        return len(self.find_files(path, ['custom.lock'])) > 0
    
    def parse(self, path):
        # Your parsing logic
        pass
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

### Adding a New Language Detector

1. Create a new detector in `sbom_scanner/detectors/`
2. Inherit from `BaseDetector`
3. Implement required methods
4. Add to `__init__.py` and `scanner.py`
5. Add tests

## Troubleshooting

### No dependencies found

- Ensure manifest files are present in the project
- Check if files are in skipped directories (`node_modules`, `vendor`, etc.)
- Try lowering `--min-confidence` threshold

### False positives

- Increase `--min-confidence` threshold
- Check if dependencies are from nested projects in subdirectories

### XML parsing errors

- Ensure XML manifest files (pom.xml, *.csproj) are well-formed
- Check for special characters or encoding issues

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [cyclonedx-python-lib](https://github.com/CycloneDX/cyclonedx-python-lib)
- Follows [CycloneDX](https://cyclonedx.org/) specification
- Uses [Package URL (PURL)](https://github.com/package-url/purl-spec) standard

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/sbom-scanner/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/sbom-scanner/wiki)
- **Security**: Report security issues via email (security@example.com)

---

**Made with ❤️ for the open source community**

