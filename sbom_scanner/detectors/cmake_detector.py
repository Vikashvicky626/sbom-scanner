"""
CMake dependency detector
Detects dependencies from CMakeLists.txt (find_package, FetchContent, etc.)
"""
import re
from pathlib import Path
from typing import Set
from .base import BaseDetector
from ..models import Dependency, Ecosystem, DependencyType


class CMakeDetector(BaseDetector):
    """Detector for CMake C/C++ projects"""
    
    def get_manifest_files(self) -> list[str]:
        return ['CMakeLists.txt', 'cmake/dependencies.cmake']
    
    def detect(self, path: Path) -> bool:
        """Check if CMakeLists.txt exists"""
        return len(self.find_files(path, ['CMakeLists.txt'])) > 0
    
    def parse(self, path: Path) -> Set[Dependency]:
        """Parse CMake dependencies"""
        dependencies = set()
        
        # Parse CMakeLists.txt files
        cmake_files = self.find_files(path, ['CMakeLists.txt'])
        for cmake_file in cmake_files:
            dependencies.update(self._parse_cmake_file(cmake_file, path))
        
        return dependencies
    
    def _parse_cmake_file(self, file_path: Path, base_path: Path) -> Set[Dependency]:
        """Parse CMakeLists.txt file"""
        dependencies = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove CMake comments
            content = re.sub(r'#.*$', '', content, flags=re.MULTILINE)
            
            # Pattern 1: find_package(PackageName VERSION REQUIRED)
            find_packages = re.finditer(
                r'find_package\s*\(\s*([a-zA-Z0-9_\-]+)(?:\s+([0-9][0-9\.]*))?\s*[^\)]*\)',
                content,
                re.IGNORECASE
            )
            
            for match in find_packages:
                name = match.group(1)
                version = match.group(2) if match.group(2) else "*"
                
                # Skip common CMake modules that are not external dependencies
                if name.lower() in ['cmake', 'ctest', 'cpack', 'threads', 'openmp']:
                    continue
                
                dep = Dependency(
                    name=name,
                    version=version,
                    ecosystem=Ecosystem.CMAKE,
                    purl=f"pkg:cmake/{name}@{version}" if version != "*" else f"pkg:cmake/{name}",
                    dependency_type=DependencyType.DIRECT,
                    source_file=str(file_path.relative_to(base_path)),
                    confidence=0.85  # Lower confidence as find_package might be system libs
                )
                dependencies.add(dep)
            
            # Pattern 2: FetchContent_Declare for external projects
            fetch_contents = re.finditer(
                r'FetchContent_Declare\s*\(\s*([a-zA-Z0-9_\-]+)\s+.*?GIT_TAG\s+([a-zA-Z0-9\.\-_]+)',
                content,
                re.DOTALL | re.IGNORECASE
            )
            
            for match in fetch_contents:
                name = match.group(1)
                version = match.group(2)  # Git tag/commit
                
                dep = Dependency(
                    name=name,
                    version=version,
                    ecosystem=Ecosystem.CMAKE,
                    purl=f"pkg:cmake/{name}@{version}",
                    dependency_type=DependencyType.DIRECT,
                    source_file=str(file_path.relative_to(base_path)),
                    confidence=0.95  # Higher confidence for FetchContent
                )
                dependencies.add(dep)
            
            # Pattern 3: ExternalProject_Add
            external_projects = re.finditer(
                r'ExternalProject_Add\s*\(\s*([a-zA-Z0-9_\-]+)',
                content,
                re.IGNORECASE
            )
            
            for match in external_projects:
                name = match.group(1)
                
                dep = Dependency(
                    name=name,
                    version="*",
                    ecosystem=Ecosystem.CMAKE,
                    purl=f"pkg:cmake/{name}",
                    dependency_type=DependencyType.DIRECT,
                    source_file=str(file_path.relative_to(base_path)),
                    confidence=0.9
                )
                dependencies.add(dep)
            
            # Pattern 4: pkg_check_modules (for pkg-config dependencies)
            pkg_checks = re.finditer(
                r'pkg_check_modules\s*\(\s*[a-zA-Z0-9_\-]+\s+(?:REQUIRED\s+)?([a-zA-Z0-9_\-]+)(?:>=([0-9\.]+))?',
                content,
                re.IGNORECASE
            )
            
            for match in pkg_checks:
                name = match.group(1)
                version = match.group(2) if match.group(2) else "*"
                
                dep = Dependency(
                    name=name,
                    version=version,
                    ecosystem=Ecosystem.CMAKE,
                    purl=f"pkg:cmake/{name}@{version}" if version != "*" else f"pkg:cmake/{name}",
                    dependency_type=DependencyType.DIRECT,
                    source_file=str(file_path.relative_to(base_path)),
                    confidence=0.85
                )
                dependencies.add(dep)
        
        except IOError as e:
            print(f"Warning: Could not parse {file_path}: {e}")
        
        return dependencies

