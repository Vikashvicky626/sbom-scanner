"""
Data models for dependency information
"""
from dataclasses import dataclass, field
from typing import Optional, List, Set
from enum import Enum


class Ecosystem(Enum):
    """Supported package ecosystems"""
    NPM = "npm"
    PYPI = "pypi"
    MAVEN = "maven"
    GRADLE = "gradle"
    COMPOSER = "composer"
    NUGET = "nuget"
    GEM = "gem"
    CARGO = "cargo"
    GO = "golang"
    COCOAPODS = "cocoapods"
    SWIFT = "swift"
    CONAN = "conan"
    VCPKG = "vcpkg"
    PLATFORMIO = "platformio"
    ARDUINO = "arduino"
    MBED = "mbed"
    CMAKE = "cmake"
    UNKNOWN = "unknown"


class DependencyType(Enum):
    """Type of dependency"""
    DIRECT = "direct"
    TRANSITIVE = "transitive"
    DEV = "development"


@dataclass
class Dependency:
    """Represents a single dependency"""
    name: str
    version: str
    ecosystem: Ecosystem
    purl: Optional[str] = None
    dependency_type: DependencyType = DependencyType.DIRECT
    source_file: Optional[str] = None
    description: Optional[str] = None
    license: Optional[str] = None
    homepage: Optional[str] = None
    confidence: float = 1.0  # 0.0 to 1.0, helps filter false positives
    
    def __hash__(self):
        return hash((self.name, self.version, self.ecosystem.value))
    
    def __eq__(self, other):
        if not isinstance(other, Dependency):
            return False
        return (self.name == other.name and 
                self.version == other.version and 
                self.ecosystem == other.ecosystem)


@dataclass
class ScanResult:
    """Result of scanning a project"""
    project_name: str
    project_version: Optional[str] = "1.0.0"
    dependencies: Set[Dependency] = field(default_factory=set)
    scan_path: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    
    def add_dependency(self, dep: Dependency):
        """Add a dependency to the result set"""
        self.dependencies.add(dep)
    
    def add_error(self, error: str):
        """Add an error message"""
        self.errors.append(error)

