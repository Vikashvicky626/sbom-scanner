# Changelog

All notable changes to SBOM Scanner will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-19

### Added
- ✨ Initial release of SBOM Scanner
- 🎯 Multi-language dependency detection (9 languages supported)
  - JavaScript/TypeScript (npm, yarn, pnpm)
  - Python (pip, poetry, pipenv)
  - Java (Maven, Gradle)
  - PHP (Composer)
  - .NET (NuGet)
  - Ruby (Gem/Bundler)
  - Rust (Cargo)
  - Go (Go modules)
- 📋 CycloneDX BOM generation (JSON and XML formats)
- 🎨 False positive reduction mechanisms
  - Confidence scoring system (0.0-1.0)
  - Automatic vendor directory filtering
  - Intelligent deduplication
  - Version normalization
- 🖥️ Command-line interface with colorful output
- 🔧 Configurable confidence threshold
- 📦 Package URL (PURL) generation for all dependencies
- 🚀 Recursive directory scanning
- ⚡ Optimized performance for large projects
- 📊 Detailed scan summaries and statistics
- 🐍 Programmatic Python API

### Detectors Implemented
- `NpmDetector` - Parses package.json, package-lock.json, yarn.lock, pnpm-lock.yaml
- `PythonDetector` - Parses requirements.txt, setup.py, Pipfile, pyproject.toml
- `MavenDetector` - Parses pom.xml with XML namespace handling
- `GradleDetector` - Parses build.gradle, build.gradle.kts with regex patterns
- `ComposerDetector` - Parses composer.json, composer.lock
- `NuGetDetector` - Parses packages.config, *.csproj, *.fsproj
- `RubyDetector` - Parses Gemfile, Gemfile.lock, *.gemspec
- `RustDetector` - Parses Cargo.toml, Cargo.lock
- `GoDetector` - Parses go.mod, go.sum

### Documentation
- 📖 Comprehensive README.md with examples
- 🚀 QUICKSTART.md for rapid onboarding
- 📚 USAGE.md with detailed usage scenarios
- 🤝 CONTRIBUTING.md with contribution guidelines
- 📝 PROJECT_SUMMARY.md with architecture overview
- ⚖️ LICENSE file (MIT)

### Examples
- Example multi-language project with sample manifest files
- Programmatic usage examples
- CI/CD integration examples (GitHub Actions, GitLab CI, Jenkins)

### Installation
- Python package with pip installation
- Installation scripts for Windows (PowerShell) and Unix (Bash)
- Development setup documentation

### Testing
- Test runner script (test_scanner.py)
- Example project for validation
- Detector verification tests

### Features Detail

#### False Positive Reduction
- **Confidence Scoring**: Each dependency assigned a confidence value
- **Directory Filtering**: Skips node_modules, vendor, venv, build directories
- **Deduplication**: Removes duplicate dependencies intelligently
- **Version Cleaning**: Normalizes version specifiers (^, ~, >=, etc.)
- **Configurable Threshold**: User-adjustable minimum confidence level

#### CycloneDX Output
- Compliant with CycloneDX v1.5 specification
- JSON format (default)
- XML format (optional)
- Complete component metadata
- Package URLs for all dependencies
- Tool information included

#### CLI Features
- Colorful, user-friendly output (via colorama)
- Progress indicators
- Detailed error messages
- Verbose mode for debugging
- Project metadata options (name, version)
- Flexible output path and format

### Technical Details

#### Architecture
- Modular detector system with base class
- Strategy pattern for detector selection
- Set-based dependency deduplication
- Streaming file parsing for memory efficiency

#### Dependencies
```
packageurl-python==0.15.6
cyclonedx-python-lib==7.5.1
pyyaml==6.0.2
toml==0.10.2
packaging==24.1
click==8.1.7
colorama==0.4.6
```

#### Python Support
- Python 3.8+
- Cross-platform (Windows, Linux, macOS)

### Known Limitations
- Does not resolve transitive dependencies (only direct dependencies)
- Lock file parsing may miss some edge cases
- Some exotic version specifiers may not parse correctly
- Large monorepos may take longer to scan

### Performance
- Optimized for projects with 100-10,000 dependencies
- Automatic skipping of vendor directories improves speed
- Recursive file search with path filtering

## [Unreleased]

### Planned Features
- [ ] SPDX format output
- [ ] Transitive dependency resolution
- [ ] License detection and reporting
- [ ] Vulnerability scanning integration
- [ ] Docker image scanning
- [ ] GitHub Action
- [ ] REST API server
- [ ] Configuration file support (.sbom-scanner.yaml)
- [ ] HTML report generation
- [ ] Swift/CocoaPods support
- [ ] Dart/Flutter support
- [ ] Additional output formats (CSV, Markdown)
- [ ] Dependency graph visualization
- [ ] Parallel scanning for large projects
- [ ] Plugin system for custom detectors
- [ ] Cache mechanism for faster re-scans

### Under Consideration
- Integration with popular security tools
- SBOM comparison/diff functionality
- SBOM merge capabilities for monorepos
- Binary/compiled artifact scanning
- Container image layer analysis
- NPM workspace support
- Yarn Berry (v2+) support
- Poetry lock file parsing
- Maven dependency tree parsing
- Gradle dependency lock files

---

## Release Notes Template

### [X.Y.Z] - YYYY-MM-DD

#### Added
- New features

#### Changed
- Changes in existing functionality

#### Deprecated
- Soon-to-be removed features

#### Removed
- Removed features

#### Fixed
- Bug fixes

#### Security
- Security fixes

---

## Version History

- **1.0.0** (2025-10-19): Initial release with 9-language support
- **Future versions**: See [Unreleased] section

## Links

- [Homepage](https://github.com/yourusername/sbom-scanner)
- [Issue Tracker](https://github.com/yourusername/sbom-scanner/issues)
- [Releases](https://github.com/yourusername/sbom-scanner/releases)

---

*For detailed usage instructions, see [README.md](README.md)*

