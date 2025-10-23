# SBOM Scanner - Project Summary

## Overview

**SBOM Scanner** is a comprehensive, multi-language dependency scanner that generates Software Bill of Materials (SBOM) in CycloneDX format with minimal false positives.

## 🎯 Key Features

### 1. Multi-Language Support
- **JavaScript/TypeScript**: npm, yarn, pnpm
- **Python**: pip, poetry, pipenv  
- **Java**: Maven, Gradle
- **PHP**: Composer
- **.NET**: NuGet
- **Ruby**: Gem/Bundler
- **Rust**: Cargo
- **Go**: Go modules

### 2. False Positive Reduction
- Confidence scoring for each dependency (0.0-1.0)
- Automatic filtering of vendor/dependency directories
- Intelligent deduplication across manifest files
- Version normalization and cleaning
- Configurable confidence threshold (default: 0.8)

### 3. Industry-Standard Output
- CycloneDX format (v1.5)
- JSON and XML output formats
- Package URL (PURL) for each dependency
- Full metadata preservation
- Compatible with security tools

### 4. Easy to Use
- Simple CLI interface
- Sensible defaults
- Colorful, informative output
- Programmatic API available
- Cross-platform (Windows, Linux, Mac)

## 📁 Project Structure

```
sbom-scanner/
├── sbom_scanner/                    # Main package
│   ├── __init__.py                  # Package info
│   ├── models.py                    # Data models (Dependency, ScanResult)
│   ├── scanner.py                   # Core scanner orchestration
│   ├── cyclonedx_generator.py      # CycloneDX BOM generation
│   ├── cli.py                       # Command-line interface
│   └── detectors/                   # Language-specific detectors
│       ├── __init__.py
│       ├── base.py                  # Base detector class
│       ├── npm_detector.py          # JavaScript/Node.js
│       ├── python_detector.py       # Python
│       ├── maven_detector.py        # Maven
│       ├── gradle_detector.py       # Gradle
│       ├── composer_detector.py     # PHP
│       ├── nuget_detector.py        # .NET
│       ├── ruby_detector.py         # Ruby
│       ├── rust_detector.py         # Rust
│       └── go_detector.py           # Go
│
├── examples/                        # Usage examples
│   ├── example_usage.py            # Programmatic usage
│   └── multi_language_project/     # Test project
│       ├── package.json
│       ├── requirements.txt
│       ├── pom.xml
│       └── go.mod
│
├── requirements.txt                 # Python dependencies
├── setup.py                        # Package setup
├── .gitignore                      # Git ignore rules
│
├── README.md                       # Full documentation
├── QUICKSTART.md                   # 5-minute guide
├── USAGE.md                        # Detailed usage
├── CONTRIBUTING.md                 # Contribution guide
├── LICENSE                         # MIT License
│
├── test_scanner.py                 # Test script
├── install.sh                      # Linux/Mac installer
├── install.ps1                     # Windows installer
└── config.example.yaml             # Configuration example
```

## 🔧 Technical Architecture

### Core Components

1. **Scanner** (`scanner.py`)
   - Orchestrates all detectors
   - Manages confidence filtering
   - Deduplicates dependencies
   - Reduces false positives

2. **Detectors** (`detectors/`)
   - Base class defines interface
   - Language-specific implementations
   - Recursive file discovery
   - Manifest parsing

3. **Models** (`models.py`)
   - `Dependency`: Represents a single dependency
   - `ScanResult`: Contains scan results
   - `Ecosystem`: Supported package ecosystems
   - `DependencyType`: Direct, dev, transitive

4. **CycloneDX Generator** (`cyclonedx_generator.py`)
   - Converts ScanResult to CycloneDX BOM
   - Supports JSON and XML output
   - Generates Package URLs (PURL)
   - Includes metadata

5. **CLI** (`cli.py`)
   - User-friendly command-line interface
   - Colorful output
   - Progress indicators
   - Error handling

### Design Patterns

- **Strategy Pattern**: Interchangeable detectors
- **Factory Pattern**: Detector instantiation
- **Builder Pattern**: SBOM construction
- **Template Method**: Base detector class

### Data Flow

```
1. User runs: sbom-scan /path/to/project
2. Scanner initializes all detectors
3. Each detector:
   - Searches for manifest files
   - Parses dependencies
   - Assigns confidence scores
4. Scanner aggregates results
5. False positive reduction applied
6. CycloneDX generator creates BOM
7. Output saved to file
```

## 📊 Supported Manifest Files

| Language | Files Detected |
|----------|---------------|
| JavaScript | `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` |
| Python | `requirements.txt`, `setup.py`, `Pipfile`, `pyproject.toml`, `setup.cfg` |
| Java (Maven) | `pom.xml` |
| Java (Gradle) | `build.gradle`, `build.gradle.kts` |
| PHP | `composer.json`, `composer.lock` |
| .NET | `packages.config`, `*.csproj`, `*.fsproj`, `*.vbproj` |
| Ruby | `Gemfile`, `Gemfile.lock`, `*.gemspec` |
| Rust | `Cargo.toml`, `Cargo.lock` |
| Go | `go.mod`, `go.sum` |

## 🎨 False Positive Reduction Strategies

### 1. Confidence Scoring
Each dependency gets a score based on:
- Manifest file type (lock files = higher confidence)
- Version specificity (exact version = higher confidence)
- Source location (root vs nested = higher confidence)

### 2. Directory Filtering
Automatically skips:
- `node_modules`, `vendor`, `bower_components`
- `.git`, `.svn`, `.hg`
- `venv`, `env`, `virtualenv`
- `target`, `build`, `dist`
- `__pycache__`, `.pytest_cache`

### 3. Deduplication
- Removes exact duplicates (name + version + ecosystem)
- Keeps highest confidence when duplicates exist
- Handles case-insensitive matching

### 4. Version Normalization
Cleans version specifiers:
- `^1.0.0` → `1.0.0`
- `~>2.1` → `2.1`
- `>=3.0` → `3.0`

## 📦 Dependencies

```
packageurl-python==0.15.6   # Package URL generation
cyclonedx-python-lib==7.5.1 # CycloneDX BOM generation
pyyaml==6.0.2               # YAML parsing
toml==0.10.2                # TOML parsing
packaging==24.1             # Version parsing
click==8.1.7                # CLI framework
colorama==0.4.6             # Colored terminal output
```

## 🚀 Usage Examples

### Basic
```bash
sbom-scan
```

### Advanced
```bash
sbom-scan /path/to/project \
  -o sbom.json \
  -f json \
  -n "MyProject" \
  -v "1.0.0" \
  --min-confidence 0.9
```

### Programmatic
```python
from sbom_scanner.scanner import Scanner
from sbom_scanner.cyclonedx_generator import CycloneDXGenerator

scanner = Scanner(min_confidence=0.8)
result = scanner.scan(".")

generator = CycloneDXGenerator()
generator.save_to_file(result, "sbom.json", "json")
```

## 🔍 Use Cases

1. **Security Vulnerability Scanning**
   - Feed SBOM to tools like Grype, Snyk, or Dependency-Track
   - Identify vulnerable dependencies
   - Track security fixes

2. **License Compliance**
   - Generate SBOMs for compliance requirements
   - Track open source usage
   - Meet regulatory requirements (e.g., EO 14028)

3. **Dependency Management**
   - Track dependency changes over time
   - Monitor dependency count trends
   - Identify outdated packages

4. **Supply Chain Security**
   - Document software composition
   - Enable SBOM exchange with partners
   - Support transparency initiatives

5. **CI/CD Integration**
   - Automated SBOM generation
   - Gate deployments on security checks
   - Archive SBOMs with releases

## 🧪 Testing

### Test Script
```bash
python test_scanner.py
```

Tests include:
- Detector imports
- CLI functionality
- Example project scanning
- CycloneDX generation
- Expected package verification

### Manual Testing
```bash
# Test on example project
sbom-scan examples/multi_language_project

# Test on real project
sbom-scan /path/to/your/project

# Test XML output
sbom-scan -f xml -o test.xml
```

## 📈 Performance

- **Speed**: Optimized for large projects
- **Memory**: Efficient streaming parsing
- **Scalability**: Handles monorepos
- **Parallelization**: Detector-level parallelization possible

## 🔮 Future Enhancements

### Potential Features
1. **Additional Languages**
   - Swift (CocoaPods, Swift Package Manager)
   - Kotlin (Gradle)
   - Scala (sbt)
   - Dart (pub)
   - Elixir (mix)

2. **Advanced Features**
   - Transitive dependency resolution
   - License detection
   - Vulnerability scanning integration
   - Docker image scanning
   - Binary analysis

3. **Configuration**
   - YAML configuration file support
   - Per-language detector settings
   - Custom skip directories
   - Output templates

4. **Output Formats**
   - SPDX format support
   - SWID tags
   - CSV export
   - HTML reports

5. **Integration**
   - REST API server
   - GitHub Action
   - GitLab CI component
   - Docker image

## 📝 License

MIT License - See LICENSE file

## 🤝 Contributing

Contributions welcome! See CONTRIBUTING.md for:
- Development setup
- Adding new detectors
- Testing guidelines
- Code standards
- Pull request process

## 📚 Documentation

- **README.md**: Full documentation
- **QUICKSTART.md**: 5-minute getting started guide
- **USAGE.md**: Detailed usage with examples
- **CONTRIBUTING.md**: Contribution guidelines
- **config.example.yaml**: Configuration reference

## 🎓 Learning Resources

### SBOM Standards
- [CycloneDX](https://cyclonedx.org/)
- [SPDX](https://spdx.dev/)
- [NTIA SBOM](https://www.ntia.gov/sbom)

### Security Tools
- [OWASP Dependency-Track](https://dependencytrack.org/)
- [Anchore Grype](https://github.com/anchore/grype)
- [Syft](https://github.com/anchore/syft)

### Package URLs
- [PURL Specification](https://github.com/package-url/purl-spec)

## 💡 Design Decisions

### Why CycloneDX?
- Modern, actively maintained
- Broad tool support
- Comprehensive schema
- Security-focused

### Why Python?
- Rapid development
- Rich ecosystem
- Cross-platform
- Easy to extend

### Why Confidence Scoring?
- Reduces false positives
- Transparent decision making
- User controllable
- Improves accuracy

### Why Skip Vendor Directories?
- Avoids nested dependencies
- Focuses on direct deps
- Reduces noise
- Faster scanning

## 🏆 Project Goals

✅ **Achieved**
- Multi-language support (9 languages)
- CycloneDX output (JSON & XML)
- False positive reduction
- Easy-to-use CLI
- Comprehensive documentation
- Example projects
- Extensible architecture

🎯 **Future Goals**
- 95%+ detection accuracy
- Sub-second scans for small projects
- GitHub Action
- Docker image
- REST API

## 👥 Credits

Built with:
- [cyclonedx-python-lib](https://github.com/CycloneDX/cyclonedx-python-lib)
- [Click](https://click.palletsprojects.com/)
- [PackageURL Python](https://github.com/package-url/packageurl-python)

## 📞 Support

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Questions and community support
- **Email**: support@example.com
- **Documentation**: Comprehensive guides included

---

**Status**: ✅ Production Ready

**Version**: 1.0.0

**Last Updated**: 2025

**Maintainers**: Open to contributors!

