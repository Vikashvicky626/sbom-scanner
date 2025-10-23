"""
PlatformIO (Embedded/IoT) dependency detector
"""
import re
from pathlib import Path
from typing import Set
from .base import BaseDetector
from ..models import Dependency, Ecosystem, DependencyType


class PlatformIODetector(BaseDetector):
    """Detector for PlatformIO embedded/IoT projects"""
    
    def get_manifest_files(self) -> list[str]:
        return ['platformio.ini', 'library.json']
    
    def detect(self, path: Path) -> bool:
        """Check if PlatformIO manifest files exist"""
        return len(self.find_files(path, self.get_manifest_files())) > 0
    
    def parse(self, path: Path) -> Set[Dependency]:
        """Parse PlatformIO dependencies"""
        dependencies = set()
        
        # Parse platformio.ini files
        platformio_ini = self.find_files(path, ['platformio.ini'])
        for ini_file in platformio_ini:
            dependencies.update(self._parse_platformio_ini(ini_file, path))
        
        # Parse library.json files
        library_json = self.find_files(path, ['library.json'])
        for lib_file in library_json:
            dependencies.update(self._parse_library_json(lib_file, path))
        
        return dependencies
    
    def _parse_platformio_ini(self, file_path: Path, base_path: Path) -> Set[Dependency]:
        """Parse platformio.ini file"""
        dependencies = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find lib_deps lines
            # Format: lib_deps = 
            #           library-name
            #           library-name@version
            #           owner/library-name@^version
            
            lib_deps_match = re.search(r'lib_deps\s*=\s*(.*?)(?:\n\[|$)', content, re.DOTALL)
            if lib_deps_match:
                lib_deps_section = lib_deps_match.group(1)
                
                for line in lib_deps_section.split('\n'):
                    line = line.strip()
                    if not line or line.startswith(';') or line.startswith('#'):
                        continue
                    
                    # Remove leading/trailing whitespace
                    line = line.strip()
                    
                    # Pattern 1: owner/library@version
                    match = re.match(r'^([a-zA-Z0-9_\-]+)/([a-zA-Z0-9_\-]+)@([^\s]+)', line)
                    if match:
                        owner = match.group(1)
                        name = match.group(2)
                        version = self._clean_version(match.group(3))
                        full_name = f"{owner}/{name}"
                    else:
                        # Pattern 2: library@version
                        match = re.match(r'^([a-zA-Z0-9_\-\s]+)@([^\s]+)', line)
                        if match:
                            full_name = match.group(1).strip()
                            version = self._clean_version(match.group(2))
                        else:
                            # Pattern 3: just library name
                            if re.match(r'^[a-zA-Z0-9_\-\s/]+$', line):
                                full_name = line.strip()
                                version = "*"
                            else:
                                continue
                    
                    if full_name:
                        dep = Dependency(
                            name=full_name,
                            version=version,
                            ecosystem=Ecosystem.PLATFORMIO,
                            purl=f"pkg:platformio/{full_name}@{version}" if version != "*" else f"pkg:platformio/{full_name}",
                            dependency_type=DependencyType.DIRECT,
                            source_file=str(file_path.relative_to(base_path)),
                            confidence=0.95
                        )
                        dependencies.add(dep)
        
        except IOError as e:
            print(f"Warning: Could not parse {file_path}: {e}")
        
        return dependencies
    
    def _parse_library_json(self, file_path: Path, base_path: Path) -> Set[Dependency]:
        """Parse library.json file"""
        dependencies = set()
        
        try:
            import json
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Parse dependencies
            if 'dependencies' in data:
                deps_data = data['dependencies']
                
                # Can be array or object
                if isinstance(deps_data, list):
                    for dep_entry in deps_data:
                        if isinstance(dep_entry, dict):
                            name = dep_entry.get('name', '')
                            version = dep_entry.get('version', '*')
                            
                            # Handle owner/name format
                            owner = dep_entry.get('owner', '')
                            if owner:
                                name = f"{owner}/{name}"
                        elif isinstance(dep_entry, str):
                            name = dep_entry
                            version = "*"
                        else:
                            continue
                        
                        if name:
                            dep = Dependency(
                                name=name,
                                version=version,
                                ecosystem=Ecosystem.PLATFORMIO,
                                purl=f"pkg:platformio/{name}@{version}" if version != "*" else f"pkg:platformio/{name}",
                                dependency_type=DependencyType.DIRECT,
                                source_file=str(file_path.relative_to(base_path)),
                                confidence=1.0
                            )
                            dependencies.add(dep)
                
                elif isinstance(deps_data, dict):
                    for name, version_spec in deps_data.items():
                        if isinstance(version_spec, str):
                            version = self._clean_version(version_spec)
                        elif isinstance(version_spec, dict):
                            version = version_spec.get('version', '*')
                        else:
                            version = "*"
                        
                        dep = Dependency(
                            name=name,
                            version=version,
                            ecosystem=Ecosystem.PLATFORMIO,
                            purl=f"pkg:platformio/{name}@{version}" if version != "*" else f"pkg:platformio/{name}",
                            dependency_type=DependencyType.DIRECT,
                            source_file=str(file_path.relative_to(base_path)),
                            confidence=1.0
                        )
                        dependencies.add(dep)
        
        except Exception as e:
            print(f"Warning: Could not parse {file_path}: {e}")
        
        return dependencies
    
    def _clean_version(self, version: str) -> str:
        """Remove version prefixes like ^, ~, >=, etc."""
        version = version.strip()
        for prefix in ['^', '~', '>=', '<=', '>', '<', '=']:
            if version.startswith(prefix):
                version = version[len(prefix):].strip()
        return version if version else "*"

