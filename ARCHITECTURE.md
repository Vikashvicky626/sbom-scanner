# SBOM Scanner Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        SBOM Scanner                         │
│                     Multi-Language SBOM Tool                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      CLI Interface                          │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  • Command-line argument parsing (Click)              │ │
│  │  • User input validation                              │ │
│  │  • Colorful output formatting                         │ │
│  │  • Progress indicators                                │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Core Scanner                            │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  1. Initialize detectors                              │ │
│  │  2. Scan project directory                            │ │
│  │  3. Aggregate results from all detectors              │ │
│  │  4. Apply false positive reduction                    │ │
│  │  5. Generate ScanResult object                        │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Language Detectors                       │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │   NPM    │  Python  │  Maven   │ Gradle   │ Composer │  │
│  │ Detector │ Detector │ Detector │ Detector │ Detector │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
│  ┌──────────┬──────────┬──────────┬──────────┐             │
│  │  NuGet   │   Ruby   │   Rust   │    Go    │             │
│  │ Detector │ Detector │ Detector │ Detector │             │
│  └──────────┴──────────┴──────────┴──────────┘             │
│                                                             │
│  Each detector:                                             │
│  • Searches for manifest files                             │
│  • Parses dependencies                                      │
│  • Assigns confidence scores                               │
│  • Returns Set[Dependency]                                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              False Positive Reduction                       │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  • Filter by confidence threshold (default 0.8)       │ │
│  │  • Deduplicate by name+version+ecosystem              │ │
│  │  • Remove dependencies from vendor directories        │ │
│  │  • Normalize version specifiers                       │ │
│  │  • Keep highest confidence for duplicates             │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                CycloneDX BOM Generator                      │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  • Convert ScanResult to CycloneDX format             │ │
│  │  • Generate Package URLs (PURL)                       │ │
│  │  • Add metadata (tool info, project info)             │ │
│  │  • Serialize to JSON or XML                           │ │
│  │  • Save to file                                       │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  sbom.json/xml   │
                    │  (CycloneDX BOM) │
                    └──────────────────┘
```

## Component Details

### 1. Data Models (`models.py`)

```
┌────────────────────────────────────────────┐
│              Ecosystem (Enum)              │
├────────────────────────────────────────────┤
│ • NPM, PYPI, MAVEN, GRADLE               │
│ • COMPOSER, NUGET, GEM, CARGO, GO        │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│         DependencyType (Enum)              │
├────────────────────────────────────────────┤
│ • DIRECT: Direct dependencies            │
│ • DEV: Development dependencies          │
│ • TRANSITIVE: Transitive dependencies    │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│             Dependency (Class)             │
├────────────────────────────────────────────┤
│ • name: str                              │
│ • version: str                           │
│ • ecosystem: Ecosystem                   │
│ • purl: Optional[str]                    │
│ • dependency_type: DependencyType        │
│ • source_file: Optional[str]             │
│ • confidence: float (0.0-1.0)            │
│ • license, homepage, description         │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│            ScanResult (Class)              │
├────────────────────────────────────────────┤
│ • project_name: str                      │
│ • project_version: str                   │
│ • dependencies: Set[Dependency]          │
│ • scan_path: str                         │
│ • errors: List[str]                      │
└────────────────────────────────────────────┘
```

### 2. Base Detector (`detectors/base.py`)

```
┌─────────────────────────────────────────────────────────┐
│              BaseDetector (Abstract Class)              │
├─────────────────────────────────────────────────────────┤
│  Abstract Methods:                                      │
│  • detect(path) -> bool                                │
│    └─ Check if detector should be used                │
│                                                         │
│  • parse(path) -> Set[Dependency]                      │
│    └─ Parse dependencies from manifest files           │
│                                                         │
│  • get_manifest_files() -> List[str]                   │
│    └─ Return list of manifest file names               │
│                                                         │
│  Utility Methods:                                       │
│  • find_files(path, filenames) -> List[Path]           │
│    └─ Recursively find manifest files                  │
│                                                         │
│  • _should_skip_path(path) -> bool                     │
│    └─ Check if path should be skipped                  │
│       (node_modules, vendor, venv, etc.)               │
└─────────────────────────────────────────────────────────┘
```

### 3. Detector Flow

```
┌─────────────────────────────────────────────────────────┐
│                   Detector Workflow                     │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │ detect(path)     │
              │ returns bool     │
              └──────────────────┘
                         │
                 ┌───────┴───────┐
                 │               │
                No              Yes
                 │               │
                 │               ▼
                 │    ┌──────────────────┐
                 │    │ find_files()     │
                 │    │ Search for       │
                 │    │ manifest files   │
                 │    └──────────────────┘
                 │               │
                 │               ▼
                 │    ┌──────────────────┐
                 │    │ parse()          │
                 │    │ For each file:   │
                 │    │ • Open & parse   │
                 │    │ • Extract deps   │
                 │    │ • Create objects │
                 │    │ • Assign scores  │
                 │    └──────────────────┘
                 │               │
                 │               ▼
                 │    ┌──────────────────┐
                 │    │ Return           │
                 │    │ Set[Dependency]  │
                 │    └──────────────────┘
                 │               │
                 └───────────────┘
                         │
                         ▼
                  (End of detector)
```

### 4. Scanner Orchestration

```
┌─────────────────────────────────────────────────────────┐
│                    Scanner.scan()                       │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │ Initialize all detectors       │
        │ [NPM, Python, Maven, ...]      │
        └────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │ For each detector:             │
        │   if detect(path):             │
        │     deps = parse(path)         │
        │     filter by confidence       │
        │     add to result              │
        └────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │ Apply false positive reduction │
        │ • Deduplicate                  │
        │ • Keep highest confidence      │
        │ • Remove obvious false pos     │
        └────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │ Return ScanResult              │
        │ • project metadata             │
        │ • dependencies set             │
        │ • errors list                  │
        └────────────────────────────────┘
```

### 5. CycloneDX Generation

```
┌─────────────────────────────────────────────────────────┐
│            CycloneDXGenerator.generate()                │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │ Create BOM object              │
        │ • Set format: CycloneDX        │
        │ • Set version: 1.5             │
        └────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │ Add metadata                   │
        │ • Tool info (sbom-scanner)     │
        │ • Project component            │
        │ • Timestamp                    │
        └────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │ For each dependency:           │
        │ • Create Component             │
        │ • Generate PURL                │
        │ • Set type (library)           │
        │ • Add version                  │
        │ • Add to BOM.components        │
        └────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │ Serialize                      │
        │ • JSON: JsonV1Dot5             │
        │ • XML: XmlV1Dot5               │
        └────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │ Return serialized string       │
        │ or save to file                │
        └────────────────────────────────┘
```

## Design Patterns Used

### 1. Strategy Pattern
```
BaseDetector (Interface)
    ├── NpmDetector
    ├── PythonDetector
    ├── MavenDetector
    └── ... (9 implementations)

Allows easy addition of new language detectors
```

### 2. Template Method Pattern
```
BaseDetector defines the algorithm:
1. find_files()
2. _should_skip_path()
3. Abstract: detect(), parse()

Concrete detectors implement specific steps
```

### 3. Builder Pattern
```
CycloneDXGenerator builds BOM incrementally:
1. Create base BOM
2. Add metadata
3. Add components (dependencies)
4. Serialize
```

### 4. Singleton-like Registry
```
Scanner maintains list of detectors
Each detector registered once at initialization
```

## Data Flow Example

### Example: Scanning a Node.js Project

```
1. User runs: sbom-scan /path/to/nodejs-app

2. CLI parses args:
   path = "/path/to/nodejs-app"
   min_confidence = 0.8
   output = "sbom.json"
   format = "json"

3. Scanner initializes:
   detectors = [NpmDetector(), PythonDetector(), ...]

4. Scanner.scan():
   For NpmDetector:
     • detect() finds package.json ✓
     • find_files() returns [/path/to/nodejs-app/package.json]
     • parse() extracts:
       - express@4.18.2 (confidence: 1.0)
       - lodash@4.17.21 (confidence: 1.0)
       - jest@29.7.0 (confidence: 1.0, type: DEV)
   
   For PythonDetector:
     • detect() finds no requirements.txt ✗
     • Skipped

5. False positive reduction:
   • All deps have confidence >= 0.8 ✓
   • No duplicates found
   • Final count: 3 dependencies

6. CycloneDX generation:
   BOM = {
     "bomFormat": "CycloneDX",
     "components": [
       {
         "name": "express",
         "version": "4.18.2",
         "purl": "pkg:npm/express@4.18.2",
         "type": "library"
       },
       ...
     ]
   }

7. Save to file:
   sbom.json written ✓

8. CLI displays summary:
   ✓ 3 dependencies found
   ✓ SBOM saved to sbom.json
```

## File Processing Flow

```
Project Directory
    │
    ├── package.json          ← NpmDetector
    ├── requirements.txt      ← PythonDetector
    ├── pom.xml              ← MavenDetector
    ├── Cargo.toml           ← RustDetector
    │
    └── node_modules/        ← SKIPPED (vendor dir)
        └── express/
            └── package.json ← NOT SCANNED
```

## Confidence Scoring Logic

```
┌─────────────────────────────────────────────┐
│          Confidence Score Factors           │
├─────────────────────────────────────────────┤
│                                             │
│  1.0 = Exact version from lock file        │
│  1.0 = Direct dep from package.json        │
│  0.95 = Parsed from setup.py (Python)      │
│  0.95 = Parsed from build.gradle (Gradle)  │
│  0.9 = Peer dependencies                   │
│  0.9 = Dependencies without version        │
│                                             │
│  Filtered if < min_confidence (default 0.8)│
└─────────────────────────────────────────────┘
```

## Directory Filtering

```
Project Root
    ├── src/                  ✓ Scanned
    ├── package.json          ✓ Scanned
    ├── node_modules/         ✗ SKIPPED
    ├── vendor/               ✗ SKIPPED
    ├── venv/                 ✗ SKIPPED
    ├── .git/                 ✗ SKIPPED
    ├── build/                ✗ SKIPPED
    ├── dist/                 ✗ SKIPPED
    └── target/               ✗ SKIPPED
```

## Extension Points

### Adding a New Detector

```
1. Create: sbom_scanner/detectors/newlang_detector.py
2. Implement: NewLangDetector(BaseDetector)
3. Register in: detectors/__init__.py
4. Add to Scanner: scanner.py
5. Add Ecosystem: models.py (if needed)
6. Test: Create test cases
```

### Adding a New Output Format

```
1. Create: sbom_scanner/formatters/new_format.py
2. Implement: NewFormatGenerator
3. Add to CLI: cli.py --format option
4. Document: Update README.md
```

## Performance Considerations

```
┌─────────────────────────────────────────────┐
│          Performance Optimizations          │
├─────────────────────────────────────────────┤
│                                             │
│  • Set-based deduplication (O(1) lookup)   │
│  • Directory skipping (reduces I/O)        │
│  • Streaming file parsing (low memory)     │
│  • Early exit on detector.detect()         │
│  • Compiled regex patterns                 │
│  • Minimal dependency tree (fast startup)  │
│                                             │
└─────────────────────────────────────────────┘
```

## Security Considerations

```
┌─────────────────────────────────────────────┐
│          Security Best Practices            │
├─────────────────────────────────────────────┤
│                                             │
│  ✓ No code execution (only parsing)        │
│  ✓ Path traversal protection               │
│  ✓ Safe XML parsing (defusedxml-like)      │
│  ✓ Input validation on file paths          │
│  ✓ No network requests                     │
│  ✓ Read-only operations                    │
│                                             │
└─────────────────────────────────────────────┘
```

## Testing Strategy

```
Unit Tests (per detector)
    • Test detection
    • Test parsing
    • Test error handling
    • Test edge cases

Integration Tests
    • Test full scan workflow
    • Test CycloneDX generation
    • Test CLI interface

End-to-End Tests
    • Test on example projects
    • Test multi-language projects
    • Verify output format
```

---

**This architecture document provides a comprehensive view of the SBOM Scanner's design and implementation.**

