# C/C++ and Embedded Device Language Support

## Overview

SBOM Scanner now includes comprehensive support for C, C++, and embedded device languages. This document details the supported package managers, build systems, and IoT/embedded platforms.

---

## 🔧 C/C++ Package Managers

### 1. Conan

**Description**: Modern C/C++ package manager  
**Ecosystem**: `conan`  
**Official Site**: https://conan.io/

#### Supported Files
- `conanfile.txt` - Simple dependency file
- `conanfile.py` - Python-based configuration
- `conan.lock` - Lock file with exact versions (highest confidence)

#### Example: conanfile.txt
```ini
[requires]
boost/1.82.0
zlib/1.2.13
openssl/3.0.0

[generators]
cmake
```

#### Example: conanfile.py
```python
from conan import ConanFile

class MyProjectConan(ConanFile):
    requires = (
        "boost/1.82.0",
        "zlib/1.2.13",
        "openssl/3.0.0"
    )
    
    def requirements(self):
        self.requires("fmt/10.0.0")
```

#### Detection Features
- Parses version specifications (e.g., `package/1.0.0@user/channel`)
- Handles both simple format (conanfile.txt) and Python format (conanfile.py)
- Lock file parsing for exact dependency versions
- High confidence scores (0.95-1.0)

---

### 2. vcpkg

**Description**: Microsoft's C/C++ package manager  
**Ecosystem**: `vcpkg`  
**Official Site**: https://vcpkg.io/

#### Supported Files
- `vcpkg.json` - Manifest mode configuration
- `vcpkg-configuration.json` - Registry configuration

#### Example: vcpkg.json
```json
{
  "name": "my-application",
  "version": "1.0.0",
  "dependencies": [
    "fmt",
    "spdlog",
    {
      "name": "boost-system",
      "version>=": "1.80.0"
    }
  ],
  "dev-dependencies": [
    "gtest"
  ]
}
```

#### Detection Features
- Parses string dependencies (no version) and object dependencies (with version)
- Supports version constraints (`version>=`, `version-string`)
- Distinguishes between direct and dev dependencies
- Confidence scores: 0.9-1.0

---

### 3. CMake

**Description**: Cross-platform build system generator  
**Ecosystem**: `cmake`  
**Official Site**: https://cmake.org/

#### Supported Files
- `CMakeLists.txt` - Main CMake configuration
- `cmake/dependencies.cmake` - Separate dependency files

#### Example: CMakeLists.txt
```cmake
cmake_minimum_required(VERSION 3.15)
project(MyProject)

# find_package with version
find_package(Boost 1.75 REQUIRED COMPONENTS system filesystem)
find_package(OpenSSL 3.0 REQUIRED)

# FetchContent for external projects
include(FetchContent)
FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG v1.14.0
)

# ExternalProject_Add
ExternalProject_Add(
  json
  GIT_REPOSITORY https://github.com/nlohmann/json.git
)

# pkg-config modules
pkg_check_modules(LIBUSB REQUIRED libusb-1.0>=1.0.20)
```

#### Detection Features
- **find_package()**: Detects package name and optional version
- **FetchContent_Declare()**: Extracts package name and GIT_TAG as version
- **ExternalProject_Add()**: Detects external project dependencies
- **pkg_check_modules()**: Detects pkg-config dependencies with versions
- Filters out CMake built-in modules (CTest, CPack, etc.)
- Confidence scores: 0.85-0.95 (lower for find_package as they might be system libs)

#### Notes
- CMake dependencies can be system libraries or external packages
- find_package() has lower confidence (0.85) as it might reference system packages
- FetchContent has higher confidence (0.95) as it explicitly fetches external code

---

## 📟 Embedded Device Languages

### 4. PlatformIO

**Description**: Professional embedded development platform for IoT  
**Ecosystem**: `platformio`  
**Official Site**: https://platformio.org/

#### Supported Files
- `platformio.ini` - Project configuration
- `library.json` - Library manifest

#### Example: platformio.ini
```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino

lib_deps =
    bblanchon/ArduinoJson@^6.21.0
    knolleary/PubSubClient@^2.8
    adafruit/Adafruit Sensor@^1.1.14
    DHT sensor library
```

#### Example: library.json
```json
{
  "name": "MySensor",
  "version": "1.0.0",
  "dependencies": [
    {
      "owner": "bblanchon",
      "name": "ArduinoJson",
      "version": "^6.21.0"
    },
    {
      "name": "DHT sensor library"
    }
  ]
}
```

#### Detection Features
- Parses `lib_deps` from platformio.ini
- Supports multiple formats:
  - `library-name`
  - `library-name@version`
  - `owner/library-name@version`
- Handles library.json dependencies (array or object format)
- Version operator cleaning (^, ~, >=, etc.)
- Confidence scores: 0.95-1.0

#### Supported Platforms
- ESP32, ESP8266
- Arduino boards
- STM32
- nRF series
- Raspberry Pi Pico
- And 40+ other platforms

---

### 5. Arduino

**Description**: Open-source electronics platform  
**Ecosystem**: `arduino`  
**Official Site**: https://www.arduino.cc/

#### Supported Files
- `library.properties` - Arduino library manifest

#### Example: library.properties
```properties
name=MySensor
version=1.0.0
author=John Doe
maintainer=John Doe <john@example.com>
sentence=A sensor library
paragraph=More detailed description
category=Sensors
url=https://github.com/user/MySensor
architectures=*
depends=Adafruit Unified Sensor, DHT sensor library (>=1.4.0)
```

#### Detection Features
- Parses `depends` field with comma-separated libraries
- Supports version specifications in parentheses: `Library (>=1.0.0)`
- Handles multiple formats:
  - `Library`
  - `Library (1.0.0)`
  - `Library (>=1.0.0)`
- Confidence score: 0.95

#### Common Libraries
- Adafruit sensors
- WiFi, Ethernet
- Servo, Stepper
- LCD, OLED displays
- And thousands more

---

### 6. Mbed OS

**Description**: ARM's embedded operating system  
**Ecosystem**: `mbed`  
**Official Site**: https://os.mbed.com/

#### Supported Files
- `mbed_lib.json` - Library configuration
- `mbed_app.json` - Application configuration
- `*.lib` - Library reference files (URLs to repositories)

#### Example: mbed_lib.json
```json
{
  "name": "my-library",
  "config": {
    "buffer-size": 1024
  },
  "dependencies": [
    "mbed-http",
    "mbed-mqtt"
  ]
}
```

#### Example: mbed_app.json
```json
{
  "target_overrides": {
    "*": {
      "platform.stdio-baud-rate": 115200
    }
  },
  "requires": [
    "mbed-http",
    "NetworkInterface"
  ]
}
```

#### Example: library.lib
```
https://github.com/ARMmbed/mbed-http/#abc123
```

#### Detection Features
- Parses `dependencies` from mbed_lib.json
- Parses `requires` from mbed_app.json
- Extracts library references from .lib files
- Attempts to parse version/revision from URLs (#tag)
- Confidence scores: 0.9-0.95

#### Target Hardware
- ARM Cortex-M microcontrollers
- STM32 families
- Nordic nRF series
- NXP Kinetis
- Silicon Labs EFM32
- And many more ARM-based boards

---

## 🎯 Key Features

### Universal C/C++ Support
- **Conan**: Modern, cross-platform package management
- **vcpkg**: Microsoft's package manager with 1500+ packages
- **CMake**: Universal build system with dependency detection

### Complete Embedded/IoT Coverage
- **PlatformIO**: 40+ platforms, 1000+ libraries
- **Arduino**: World's most popular embedded platform
- **Mbed OS**: Professional ARM development

### Smart Detection
- Multiple manifest file formats
- Version constraint parsing
- Confidence scoring to reduce false positives
- Support for lock files (exact versions)

### False Positive Reduction
- Skips build directories (`build/`, `cmake-build-*/`, etc.)
- Filters CMake built-in modules
- Validates package name formats
- Confidence thresholds (0.85-1.0)

---

## 📊 Confidence Scores

| Detector | File Type | Confidence | Reason |
|----------|-----------|------------|---------|
| Conan | conan.lock | 1.0 | Lock file with exact versions |
| Conan | conanfile.txt | 1.0 | Explicit dependency list |
| Conan | conanfile.py | 0.95 | Requires parsing Python code |
| vcpkg | vcpkg.json (with version) | 1.0 | Explicit version specified |
| vcpkg | vcpkg.json (no version) | 0.9 | No version specified |
| CMake | FetchContent | 0.95 | Explicit external fetch |
| CMake | ExternalProject | 0.9 | External project reference |
| CMake | find_package | 0.85 | Might be system library |
| PlatformIO | library.json | 1.0 | Structured dependency file |
| PlatformIO | platformio.ini | 0.95 | Parsed from INI format |
| Arduino | library.properties | 0.95 | Official library format |
| Mbed | mbed_lib.json | 0.95 | Structured JSON |
| Mbed | mbed_app.json | 0.95 | Application manifest |
| Mbed | *.lib | 0.9 | URL reference only |

---

## 🔄 Package URL (PURL) Format

### Standard Format
```
pkg:conan/boost@1.82.0
pkg:vcpkg/fmt@10.0.0
pkg:cmake/OpenSSL@3.0.0
pkg:platformio/ArduinoJson@6.21.0
pkg:arduino/Adafruit-Sensor@1.1.14
pkg:mbed/mbed-http
```

### For Generic/Unknown Versions
```
pkg:conan/zlib
pkg:vcpkg/gtest
pkg:arduino/Servo
```

---

## 📝 Usage Examples

### Scan a Conan Project
```bash
sbom-scan /path/to/conan-project -o sbom.json
```

### Scan a PlatformIO IoT Project
```bash
sbom-scan /path/to/platformio-project -o embedded-sbom.json
```

### Scan Arduino Project
```bash
sbom-scan /path/to/arduino-sketch -o arduino-sbom.json
```

### Scan CMake Project
```bash
sbom-scan /path/to/cmake-project -o sbom.json
```

### Adjust Confidence for C/C++ Projects
```bash
# Strict mode (only high-confidence deps)
sbom-scan --min-confidence 0.9

# Include CMake find_package calls
sbom-scan --min-confidence 0.85
```

---

## 🧪 Example Projects

### Conan Example
```
my-cpp-project/
├── conanfile.txt
├── CMakeLists.txt
└── src/
    └── main.cpp
```

**conanfile.txt:**
```ini
[requires]
boost/1.82.0
openssl/3.0.0
```

**Scan:**
```bash
sbom-scan my-cpp-project
```

**Result:**
- boost@1.82.0 (conan)
- openssl@3.0.0 (conan)

---

### PlatformIO Example
```
my-iot-device/
├── platformio.ini
├── src/
│   └── main.cpp
└── lib/
```

**platformio.ini:**
```ini
[env:esp32]
platform = espressif32
lib_deps =
    bblanchon/ArduinoJson@^6.21.0
    PubSubClient
```

**Scan:**
```bash
sbom-scan my-iot-device
```

**Result:**
- bblanchon/ArduinoJson@6.21.0 (platformio)
- PubSubClient@* (platformio)

---

### Arduino Example
```
MySensor/
├── MySensor.ino
├── library.properties
└── src/
    └── MySensor.cpp
```

**library.properties:**
```properties
name=MySensor
version=1.0.0
depends=Adafruit Unified Sensor, DHT sensor library
```

**Scan:**
```bash
sbom-scan MySensor
```

**Result:**
- Adafruit Unified Sensor@* (arduino)
- DHT sensor library@* (arduino)

---

## 🎓 Best Practices

### 1. Use Lock Files
- **Conan**: Use `conan.lock` for reproducible builds
- **vcpkg**: Commit `vcpkg.json` with exact versions

### 2. Specify Versions
```ini
# Good
[requires]
boost/1.82.0

# Less precise
[requires]
boost/[>=1.80.0]
```

### 3. Organize Dependencies
- Keep dependencies in root manifest files
- Avoid nested conanfiles in subdirectories
- Use consistent version pinning strategy

### 4. Confidence Thresholds
- **Production**: Use `--min-confidence 0.9` for strict filtering
- **Development**: Use `--min-confidence 0.8` (default)
- **Analysis**: Use `--min-confidence 0.7` to catch all possibilities

### 5. Regular Scanning
```bash
# Add to CI/CD
sbom-scan -o sbom.json
```

---

## 🔗 Integration with Security Tools

Generated SBOMs are compatible with:
- **Grype**: Vulnerability scanning
- **Dependency-Track**: OWASP dependency monitoring
- **Trivy**: Security scanner
- **Snyk**: Security platform
- **WhiteSource**: License compliance

**Example:**
```bash
# Generate SBOM
sbom-scan -o sbom.json

# Scan for vulnerabilities
grype sbom:sbom.json
```

---

## 🚀 What's New

### Added Support For:
1. ✅ **Conan** - Modern C/C++ package manager
2. ✅ **vcpkg** - Microsoft's C/C++ library manager
3. ✅ **CMake** - Build system with dependency detection
4. ✅ **PlatformIO** - Embedded/IoT development platform
5. ✅ **Arduino** - Popular embedded electronics platform
6. ✅ **Mbed OS** - ARM embedded operating system

### Total Language Support: **15 Languages/Platforms**
- 9 Original languages (JS, Python, Java, PHP, .NET, Ruby, Rust, Go)
- 6 New C/C++/Embedded platforms

---

## 📖 Further Reading

- [Conan Documentation](https://docs.conan.io/)
- [vcpkg Documentation](https://vcpkg.io/en/getting-started.html)
- [CMake Documentation](https://cmake.org/documentation/)
- [PlatformIO Docs](https://docs.platformio.org/)
- [Arduino Libraries](https://www.arduino.cc/reference/en/libraries/)
- [Mbed OS Documentation](https://os.mbed.com/docs/)

---

**The SBOM Scanner now provides comprehensive coverage for C, C++, and all major embedded device platforms!** 🎉

