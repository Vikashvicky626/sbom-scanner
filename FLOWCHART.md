# SBOM Scanner - System Flowchart

## High-Level Overview

```mermaid
flowchart TB
    Start([User runs sbom-scan]) --> CLI[CLI Interface<br/>Parse Arguments]
    CLI --> Init[Initialize Scanner<br/>min_confidence=0.8]
    Init --> LoadDet[Load All Detectors<br/>15 Language Detectors]
    LoadDet --> Scan[Start Scan Process]
    Scan --> Detect{For Each Detector:<br/>Check if Project<br/>Uses This Language}
    Detect -->|Yes| Parse[Parse Dependencies<br/>from Manifest Files]
    Detect -->|No| NextDet[Try Next Detector]
    NextDet --> Detect
    Parse --> Collect[Collect Dependencies<br/>with Confidence Scores]
    Collect --> NextDet
    Detect -->|All Done| Filter[Apply False Positive<br/>Reduction]
    Filter --> Dedup[Deduplicate<br/>Dependencies]
    Dedup --> GenBOM[Generate CycloneDX<br/>BOM]
    GenBOM --> Output[Save to File<br/>JSON or XML]
    Output --> Summary[Display Summary<br/>Statistics]
    Summary --> End([Complete!])
    
    style Start fill:#90EE90
    style End fill:#90EE90
    style CLI fill:#87CEEB
    style Detect fill:#FFD700
    style Filter fill:#FFA500
    style GenBOM fill:#9370DB
    style Output fill:#FF6347
```

---

## Detailed System Flow

### 1. Command-Line Interface (CLI)

```mermaid
flowchart LR
    A([User Command]) --> B{Parse Arguments}
    B --> C[path<br/>default: .]
    B --> D[output<br/>default: sbom.json]
    B --> E[format<br/>json or xml]
    B --> F[min-confidence<br/>default: 0.8]
    B --> G[project-name<br/>optional]
    B --> H[project-version<br/>optional]
    C --> I[Validate Path]
    D --> J[Validate Output]
    E --> K[Validate Format]
    F --> L[Validate 0.0-1.0]
    I --> M{Valid?}
    J --> M
    K --> M
    L --> M
    M -->|Yes| N[Create Scanner]
    M -->|No| O([Exit with Error])
    
    style A fill:#90EE90
    style N fill:#87CEEB
    style O fill:#FF6347
```

---

### 2. Scanner Initialization

```mermaid
flowchart TB
    A[Scanner.__init__] --> B[Set min_confidence]
    B --> C[Initialize Detector List]
    C --> D1[NpmDetector]
    C --> D2[PythonDetector]
    C --> D3[MavenDetector]
    C --> D4[GradleDetector]
    C --> D5[ComposerDetector]
    C --> D6[NuGetDetector]
    C --> D7[RubyDetector]
    C --> D8[RustDetector]
    C --> D9[GoDetector]
    C --> D10[ConanDetector]
    C --> D11[VcpkgDetector]
    C --> D12[CMakeDetector]
    C --> D13[PlatformIODetector]
    C --> D14[ArduinoDetector]
    C --> D15[MbedDetector]
    D1 --> E[15 Detectors Ready]
    D2 --> E
    D3 --> E
    D4 --> E
    D5 --> E
    D6 --> E
    D7 --> E
    D8 --> E
    D9 --> E
    D10 --> E
    D11 --> E
    D12 --> E
    D13 --> E
    D14 --> E
    D15 --> E
    E --> F[Scanner Ready]
    
    style A fill:#87CEEB
    style F fill:#90EE90
```

---

### 3. Scan Process

```mermaid
flowchart TB
    A[scanner.scan<br/>path, name, version] --> B[Validate Path<br/>exists & is directory]
    B --> C[Create ScanResult<br/>object]
    C --> D[Start Detector Loop]
    D --> E{For Each<br/>Detector}
    E --> F[detector.detect<br/>path]
    F --> G{Manifest Files<br/>Found?}
    G -->|No| H[Skip This Detector]
    G -->|Yes| I[Print: ✓ Detected]
    I --> J[detector.parse<br/>path]
    J --> K[Get Set of<br/>Dependencies]
    K --> L{Filter by<br/>min_confidence}
    L -->|conf >= threshold| M[Add to Results]
    L -->|conf < threshold| N[Discard]
    M --> O[Print: Found N deps]
    N --> H
    O --> H
    H --> P{More<br/>Detectors?}
    P -->|Yes| E
    P -->|No| Q[Apply False Positive<br/>Reduction]
    Q --> R[Return ScanResult]
    
    style A fill:#87CEEB
    style G fill:#FFD700
    style L fill:#FFA500
    style R fill:#90EE90
```

---

### 4. Detector Workflow (Base Pattern)

```mermaid
flowchart TB
    A[BaseDetector] --> B[detect<br/>path]
    B --> C[Get manifest<br/>file list]
    C --> D[find_files<br/>search recursively]
    D --> E{Files Found?}
    E -->|No| F[Return False]
    E -->|Yes| G[Return True]
    
    G --> H[parse<br/>path]
    H --> I[Find all manifest<br/>files]
    I --> J{For Each File}
    J --> K[Check if<br/>should_skip_path]
    K -->|Skip| L[node_modules?<br/>vendor?<br/>venv?<br/>build?]
    K -->|Process| M[Open & Parse File]
    L --> N[Skip File]
    M --> O{Parse<br/>Success?}
    O -->|No| P[Log Warning<br/>Continue]
    O -->|Yes| Q[Extract Dependencies]
    Q --> R[Create Dependency<br/>Objects]
    R --> S[Assign Confidence<br/>Score]
    S --> T[Add to Set]
    T --> U{More Files?}
    U -->|Yes| J
    U -->|No| V[Return Set of<br/>Dependencies]
    
    style A fill:#87CEEB
    style E fill:#FFD700
    style K fill:#FFA500
    style V fill:#90EE90
```

---

### 5. Example: NPM Detector Flow

```mermaid
flowchart TB
    A[NpmDetector.detect] --> B{Find package.json<br/>in project?}
    B -->|No| C[Return False<br/>Skip NPM]
    B -->|Yes| D[Return True]
    
    D --> E[NpmDetector.parse]
    E --> F[Find all<br/>package.json files]
    F --> G{For Each File}
    G --> H[Open package.json]
    H --> I[Parse JSON]
    I --> J{Parse Error?}
    J -->|Yes| K[Log Warning<br/>Skip File]
    J -->|No| L[Process dependencies]
    
    L --> M[Parse 'dependencies']
    L --> N[Parse 'devDependencies']
    L --> O[Parse 'peerDependencies']
    
    M --> P{For Each Dep}
    P --> Q[name, version]
    Q --> R[Clean version<br/>remove ^, ~, etc]
    R --> S[Create Dependency<br/>type=DIRECT<br/>confidence=1.0]
    S --> T[Generate PURL<br/>pkg:npm/name@ver]
    T --> U[Add to Set]
    
    N --> V{For Each DevDep}
    V --> W[Create Dependency<br/>type=DEV<br/>confidence=1.0]
    W --> U
    
    O --> X{For Each PeerDep}
    X --> Y[Create Dependency<br/>type=DIRECT<br/>confidence=0.9]
    Y --> U
    
    U --> Z{More Files?}
    Z -->|Yes| G
    Z -->|No| AA[Return All<br/>Dependencies]
    
    style A fill:#87CEEB
    style B fill:#FFD700
    style AA fill:#90EE90
```

---

### 6. False Positive Reduction

```mermaid
flowchart TB
    A[All Dependencies<br/>from All Detectors] --> B[Create Empty<br/>Filtered Set]
    B --> C{For Each<br/>Dependency}
    C --> D{Confidence >=<br/>min_threshold?}
    D -->|No| E[Discard<br/>Too Low Confidence]
    D -->|Yes| F[Check for<br/>Duplicates]
    F --> G{Seen this<br/>name+ecosystem<br/>before?}
    G -->|No| H[Add to Set<br/>Track in seen dict]
    G -->|Yes| I{Same Version?}
    I -->|Yes| J{Higher<br/>Confidence?}
    I -->|No| K[Keep Both<br/>Different Versions]
    J -->|Yes| L[Replace Old<br/>with Higher Confidence]
    J -->|No| M[Keep Old]
    L --> N
    M --> N
    K --> N
    H --> N
    E --> N{More<br/>Dependencies?}
    N -->|Yes| C
    N -->|No| O[Return Filtered<br/>Deduplicated Set]
    
    style A fill:#87CEEB
    style D fill:#FFD700
    style G fill:#FFA500
    style O fill:#90EE90
```

---

### 7. CycloneDX BOM Generation

```mermaid
flowchart TB
    A[CycloneDXGenerator.generate] --> B[Create BOM Object]
    B --> C[Add Metadata]
    C --> D[Add Tool Info<br/>sbom-scanner v1.0.0]
    D --> E[Add Main Component<br/>Project Info]
    E --> F{For Each<br/>Dependency}
    F --> G[Create Component]
    G --> H{Has PURL?}
    H -->|Yes| I[Use Provided PURL]
    H -->|No| J[Construct PURL]
    J --> K[Map Ecosystem<br/>to PURL Type]
    K --> L{Maven-style<br/>group:artifact?}
    L -->|Yes| M[Split into<br/>namespace + name]
    L -->|No| N[Use name as-is]
    M --> O[Create PackageURL]
    N --> O
    I --> P[Create Component<br/>Object]
    O --> P
    P --> Q[Set name, version]
    Q --> R[Set type=library]
    R --> S[Add PURL]
    S --> T[Add to BOM.components]
    T --> U{More<br/>Dependencies?}
    U -->|Yes| F
    U -->|No| V{Output Format?}
    V -->|JSON| W[JsonV1Dot5<br/>Serialize]
    V -->|XML| X[XmlV1Dot5<br/>Serialize]
    W --> Y[Return String]
    X --> Y
    Y --> Z[Save to File]
    
    style A fill:#87CEEB
    style H fill:#FFD700
    style V fill:#FFA500
    style Z fill:#90EE90
```

---

### 8. Complete End-to-End Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER INVOCATION                            │
│  $ sbom-scan /path/to/project -o sbom.json --min-confidence 0.8│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CLI LAYER (cli.py)                         │
├─────────────────────────────────────────────────────────────────┤
│  • Parse command-line arguments                                 │
│  • Validate inputs (path exists, confidence 0-1, format)        │
│  • Create Scanner instance                                      │
│  • Display banner and status messages                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SCANNER ORCHESTRATION (scanner.py)             │
├─────────────────────────────────────────────────────────────────┤
│  1. Initialize all 15 detectors                                 │
│  2. Create ScanResult object                                    │
│  3. For each detector:                                          │
│     ├─ detect() - check if language is present                 │
│     ├─ parse() - extract dependencies if detected              │
│     └─ filter by min_confidence                                │
│  4. Aggregate all dependencies                                  │
│  5. Apply false positive reduction                              │
│  6. Return ScanResult                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              DETECTOR LAYER (detectors/*.py)                    │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│  │    NPM    │  │  Python   │  │   Maven   │  │  Gradle   │  │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│  │ Composer  │  │   NuGet   │  │   Ruby    │  │   Rust    │  │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│  │    Go     │  │   Conan   │  │  vcpkg    │  │   CMake   │  │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐                 │
│  │PlatformIO │  │  Arduino  │  │   Mbed    │                 │
│  └───────────┘  └───────────┘  └───────────┘                 │
│                                                                 │
│  Each detector:                                                 │
│  • Searches for manifest files (package.json, requirements.txt)│
│  • Parses dependencies with versions                            │
│  • Assigns confidence scores                                    │
│  • Returns Set[Dependency]                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│            DATA MODELS (models.py)                              │
├─────────────────────────────────────────────────────────────────┤
│  Dependency:                                                    │
│    • name: str                                                  │
│    • version: str                                               │
│    • ecosystem: Ecosystem (npm, pypi, maven, conan, etc.)      │
│    • purl: str (pkg:npm/express@4.18.2)                        │
│    • dependency_type: DIRECT | DEV | TRANSITIVE                │
│    • confidence: float (0.0-1.0)                                │
│    • source_file: str (package.json)                            │
│                                                                 │
│  ScanResult:                                                    │
│    • project_name: str                                          │
│    • project_version: str                                       │
│    • dependencies: Set[Dependency]                              │
│    • errors: List[str]                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│         FALSE POSITIVE REDUCTION (scanner.py)                   │
├─────────────────────────────────────────────────────────────────┤
│  1. Filter by confidence threshold (>= min_confidence)          │
│  2. Deduplicate by name + ecosystem                             │
│  3. Keep highest confidence for duplicates                      │
│  4. Remove obvious false positives                              │
│  5. Normalize versions (remove ^, ~, >=, etc.)                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│       CYCLONEDX GENERATION (cyclonedx_generator.py)             │
├─────────────────────────────────────────────────────────────────┤
│  1. Create CycloneDX BOM object                                 │
│  2. Add metadata (tool, project component)                      │
│  3. For each dependency:                                        │
│     ├─ Create Component object                                 │
│     ├─ Generate/use Package URL (PURL)                         │
│     ├─ Set component type (library)                            │
│     └─ Add to BOM.components                                   │
│  4. Serialize to JSON or XML (CycloneDX v1.5)                   │
│  5. Save to file                                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUT                                     │
│  {                                                              │
│    "bomFormat": "CycloneDX",                                    │
│    "specVersion": "1.5",                                        │
│    "components": [                                              │
│      {                                                          │
│        "type": "library",                                       │
│        "name": "express",                                       │
│        "version": "4.18.2",                                     │
│        "purl": "pkg:npm/express@4.18.2"                         │
│      },                                                         │
│      ...                                                        │
│    ]                                                            │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DISPLAY SUMMARY (cli.py)                      │
├─────────────────────────────────────────────────────────────────┤
│  ✓ Scan Summary                                                 │
│    Project Name:        my-project                              │
│    Total Dependencies:  25                                      │
│                                                                 │
│    Dependencies by Ecosystem:                                   │
│      npm           : 10                                         │
│      pypi          : 8                                          │
│      maven         : 5                                          │
│      conan         : 2                                          │
│                                                                 │
│    Output: sbom.json                                            │
│  ✓ Scan completed successfully!                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Decision Flow: Confidence Scoring

```mermaid
flowchart TB
    A[Dependency Found] --> B{What File Type?}
    B -->|Lock File| C[Confidence = 1.0<br/>Exact Version]
    B -->|package.json| D[Confidence = 1.0<br/>Direct Declaration]
    B -->|conanfile.py| E[Confidence = 0.95<br/>Parsed from Python]
    B -->|CMake find_package| F[Confidence = 0.85<br/>Might be System Lib]
    B -->|No Version Specified| G[Confidence = 0.9<br/>Version Unknown]
    
    C --> H{>= min_threshold?}
    D --> H
    E --> H
    F --> H
    G --> H
    
    H -->|Yes| I[Include in SBOM]
    H -->|No| J[Discard<br/>Too Low Confidence]
    
    style A fill:#87CEEB
    style B fill:#FFD700
    style H fill:#FFA500
    style I fill:#90EE90
    style J fill:#FF6347
```

---

## File Processing Flow

```mermaid
flowchart LR
    A[Project Directory] --> B{Recursive Scan}
    B --> C[package.json]
    B --> D[requirements.txt]
    B --> E[pom.xml]
    B --> F[conanfile.txt]
    B --> G[platformio.ini]
    B --> H[...]
    
    B --> I[node_modules/]
    B --> J[vendor/]
    B --> K[venv/]
    B --> L[build/]
    
    C --> M[NpmDetector]
    D --> N[PythonDetector]
    E --> O[MavenDetector]
    F --> P[ConanDetector]
    G --> Q[PlatformIODetector]
    
    I --> R[SKIP ✗]
    J --> R
    K --> R
    L --> R
    
    M --> S[Parse & Extract]
    N --> S
    O --> S
    P --> S
    Q --> S
    
    S --> T[Dependencies Set]
    
    style A fill:#87CEEB
    style R fill:#FF6347
    style T fill:#90EE90
```

---

## Error Handling Flow

```mermaid
flowchart TB
    A[Process File] --> B{File Exists?}
    B -->|No| C[Log Warning<br/>Skip File]
    B -->|Yes| D{Can Read?}
    D -->|No| E[IOError<br/>Log Warning]
    D -->|Yes| F{Parse Success?}
    F -->|No| G[JSON/XML Error<br/>Log Warning]
    F -->|Yes| H{Valid Format?}
    H -->|No| I[Format Error<br/>Log Warning]
    H -->|Yes| J[Process<br/>Dependencies]
    
    C --> K[Continue with<br/>Next File]
    E --> K
    G --> K
    I --> K
    J --> L[Success]
    
    style A fill:#87CEEB
    style C fill:#FFA500
    style E fill:#FFA500
    style G fill:#FFA500
    style I fill:#FFA500
    style L fill:#90EE90
```

---

## Performance Optimization Flow

```mermaid
flowchart TB
    A[Scan Request] --> B[Early Detection]
    B --> C{Manifest Files<br/>Present?}
    C -->|No| D[Skip Detector<br/>Immediately]
    C -->|Yes| E[Proceed with<br/>Parsing]
    
    E --> F[Path Filtering]
    F --> G{In Skip List?<br/>node_modules<br/>vendor, etc.}
    G -->|Yes| H[Skip Directory<br/>No Recursion]
    G -->|No| I[Process Files]
    
    I --> J[Set-Based Storage]
    J --> K[O(1) Duplicate<br/>Detection]
    K --> L[Efficient<br/>Deduplication]
    
    D --> M[Fast Completion]
    H --> M
    L --> M
    
    style A fill:#87CEEB
    style C fill:#FFD700
    style G fill:#FFA500
    style M fill:#90EE90
```

---

## Summary: Three-Phase Architecture

```
┌───────────────────────────────────────────────────────────┐
│                    PHASE 1: DETECTION                     │
│  • Load all 15 detectors                                  │
│  • For each detector, check if language is present        │
│  • Quick detection using manifest file existence          │
│  • Skip detectors that don't apply                        │
└───────────────────────────────────────────────────────────┘
                          │
                          ▼
┌───────────────────────────────────────────────────────────┐
│                    PHASE 2: PARSING                       │
│  • For detected languages, parse manifest files           │
│  • Extract dependency name, version, type                 │
│  • Assign confidence scores                               │
│  • Generate Package URLs (PURL)                           │
│  • Collect all dependencies in a set                      │
└───────────────────────────────────────────────────────────┘
                          │
                          ▼
┌───────────────────────────────────────────────────────────┐
│               PHASE 3: GENERATION                         │
│  • Filter by confidence threshold                         │
│  • Deduplicate dependencies                               │
│  • Generate CycloneDX BOM (JSON/XML)                      │
│  • Save to file                                           │
│  • Display summary statistics                             │
└───────────────────────────────────────────────────────────┘
```

---

**This flowchart documentation provides a complete visual understanding of the SBOM Scanner's architecture and operation!** 🎨

