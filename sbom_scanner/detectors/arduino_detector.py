"""
Arduino dependency detector
"""
import json
import re
from pathlib import Path
from typing import Set
from .base import BaseDetector
from ..models import Dependency, Ecosystem, DependencyType


class ArduinoDetector(BaseDetector):
    """Detector for Arduino projects"""
    
    def get_manifest_files(self) -> list[str]:
        return ['library.properties', 'library.json']
    
    def detect(self, path: Path) -> bool:
        """Check if Arduino manifest files exist"""
        return len(self.find_files(path, ['library.properties'])) > 0
    
    def parse(self, path: Path) -> Set[Dependency]:
        """Parse Arduino dependencies"""
        dependencies = set()
        
        # Parse library.properties files
        lib_props = self.find_files(path, ['library.properties'])
        for prop_file in lib_props:
            dependencies.update(self._parse_library_properties(prop_file, path))
        
        return dependencies
    
    def _parse_library_properties(self, file_path: Path, base_path: Path) -> Set[Dependency]:
        """Parse library.properties file"""
        dependencies = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find depends line
            # Format: depends=Library1, Library2 (>=1.0.0), Library3
            depends_match = re.search(r'^depends\s*=\s*(.+)$', content, re.MULTILINE)
            if depends_match:
                depends_line = depends_match.group(1).strip()
                
                # Split by comma
                libraries = [lib.strip() for lib in depends_line.split(',')]
                
                for lib in libraries:
                    if not lib:
                        continue
                    
                    # Parse library name and optional version
                    # Format: "Library (>=1.0.0)" or "Library (1.0.0)" or just "Library"
                    match = re.match(r'^([a-zA-Z0-9_\-\s]+)\s*(?:\(([^\)]+)\))?', lib)
                    if match:
                        name = match.group(1).strip()
                        version_spec = match.group(2)
                        
                        if version_spec:
                            # Clean version operators
                            version = self._clean_version(version_spec)
                        else:
                            version = "*"
                        
                        dep = Dependency(
                            name=name,
                            version=version,
                            ecosystem=Ecosystem.ARDUINO,
                            purl=f"pkg:arduino/{name}@{version}" if version != "*" else f"pkg:arduino/{name}",
                            dependency_type=DependencyType.DIRECT,
                            source_file=str(file_path.relative_to(base_path)),
                            confidence=0.95
                        )
                        dependencies.add(dep)
        
        except IOError as e:
            print(f"Warning: Could not parse {file_path}: {e}")
        
        return dependencies
    
    def _clean_version(self, version: str) -> str:
        """Remove version operators"""
        version = version.strip()
        for prefix in ['>=', '<=', '>', '<', '=', '~', '^']:
            if version.startswith(prefix):
                version = version[len(prefix):].strip()
        return version if version else "*"

